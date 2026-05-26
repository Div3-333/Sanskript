use serde::Deserialize;
use std::collections::{HashMap, HashSet};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum BytecodeError {
    #[error("unsupported bytecode version: {0}")]
    UnsupportedVersion(i64),
    #[error("invalid program: {0}")]
    InvalidProgram(String),
    #[error("json: {0}")]
    Json(#[from] serde_json::Error),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    PushInt,
    PushText,
    LoadName,
    StoreName,
    Add,
    Subtract,
    Multiply,
    Divide,
    CompareEq,
    CompareLt,
    Emit,
    Jump,
    JumpIfZero,
    Call,
    Return,
    Pop,
    Halt,
}

impl OpCode {
    fn from_str(value: &str) -> Result<Self, BytecodeError> {
        match value {
            "push_int" => Ok(Self::PushInt),
            "push_text" => Ok(Self::PushText),
            "load_name" => Ok(Self::LoadName),
            "store_name" => Ok(Self::StoreName),
            "add" => Ok(Self::Add),
            "subtract" => Ok(Self::Subtract),
            "multiply" => Ok(Self::Multiply),
            "divide" => Ok(Self::Divide),
            "compare_eq" => Ok(Self::CompareEq),
            "compare_lt" => Ok(Self::CompareLt),
            "emit" => Ok(Self::Emit),
            "jump" => Ok(Self::Jump),
            "jump_if_zero" => Ok(Self::JumpIfZero),
            "call" => Ok(Self::Call),
            "return" => Ok(Self::Return),
            "pop" => Ok(Self::Pop),
            "halt" => Ok(Self::Halt),
            other => Err(BytecodeError::InvalidProgram(format!("unknown opcode: {other}"))),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Instruction {
    pub opcode: OpCode,
    pub operand: Option<Operand>,
}

#[derive(Debug, Clone)]
pub enum Operand {
    Int(i64),
    Text(String),
    Name(String),
}

#[derive(Debug, Clone)]
pub struct FunctionBytecode {
    pub name: String,
    pub instructions: Vec<Instruction>,
    pub params: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct ModuleBytecode {
    pub name: String,
    pub functions: Vec<FunctionBytecode>,
}

#[derive(Debug, Clone)]
pub struct BytecodeProgram {
    pub version: i64,
    pub instructions: Vec<Instruction>,
    pub functions: Vec<FunctionBytecode>,
    pub modules: Vec<ModuleBytecode>,
}

#[derive(Debug, Deserialize)]
struct RawInstruction {
    op: String,
    #[serde(default)]
    operand: Option<serde_json::Value>,
}

#[derive(Debug, Deserialize)]
struct RawFunction {
    name: String,
    #[serde(default)]
    params: Vec<String>,
    instructions: Vec<RawInstruction>,
}

#[derive(Debug, Deserialize)]
struct RawModule {
    name: String,
    functions: Vec<RawFunction>,
}

#[derive(Debug, Deserialize)]
struct RawProgram {
    version: i64,
    instructions: Vec<RawInstruction>,
    #[serde(default)]
    functions: Vec<RawFunction>,
    #[serde(default)]
    modules: Vec<RawModule>,
}

#[derive(Debug, Deserialize)]
pub struct ConformanceFixture {
    pub version: i64,
    pub instructions: Vec<RawInstruction>,
    #[serde(default)]
    functions: Vec<RawFunction>,
    #[serde(default)]
    modules: Vec<RawModule>,
    pub expected_output: Vec<String>,
    #[serde(default)]
    pub expected_environment: HashMap<String, i64>,
}

fn parse_instruction(raw: &RawInstruction) -> Result<Instruction, BytecodeError> {
    let opcode = OpCode::from_str(&raw.op)?;
    let operand = match opcode {
        OpCode::PushInt | OpCode::Jump | OpCode::JumpIfZero => {
            let value = raw.operand.as_ref().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} requires operand", raw.op))
            })?;
            let number = value.as_i64().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} operand must be integer", raw.op))
            })?;
            Some(Operand::Int(number))
        }
        OpCode::PushText => {
            let value = raw.operand.as_ref().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} requires operand", raw.op))
            })?;
            let text = value.as_str().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} operand must be string", raw.op))
            })?;
            Some(Operand::Text(text.to_string()))
        }
        OpCode::LoadName | OpCode::StoreName | OpCode::Call => {
            let value = raw.operand.as_ref().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} requires operand", raw.op))
            })?;
            let name = value.as_str().ok_or_else(|| {
                BytecodeError::InvalidProgram(format!("{} operand must be string", raw.op))
            })?;
            if name.is_empty() {
                return Err(BytecodeError::InvalidProgram(format!(
                    "{} operand must be non-empty",
                    raw.op
                )));
            }
            Some(Operand::Name(name.to_string()))
        }
        OpCode::Add
        | OpCode::Subtract
        | OpCode::Multiply
        | OpCode::Divide
        | OpCode::CompareEq
        | OpCode::CompareLt
        | OpCode::Emit
        | OpCode::Return
        | OpCode::Pop
        | OpCode::Halt => {
            if raw.operand.is_some() {
                return Err(BytecodeError::InvalidProgram(format!(
                    "{} must not have an operand",
                    raw.op
                )));
            }
            None
        }
    };
    Ok(Instruction { opcode, operand })
}

fn parse_function(raw: RawFunction) -> Result<FunctionBytecode, BytecodeError> {
    if raw.name.is_empty() {
        return Err(BytecodeError::InvalidProgram("function name is required".into()));
    }
    let mut seen = HashSet::new();
    for param in &raw.params {
        if param.is_empty() {
            return Err(BytecodeError::InvalidProgram(format!(
                "function {} has an empty param",
                raw.name
            )));
        }
        if !seen.insert(param.clone()) {
            return Err(BytecodeError::InvalidProgram(format!(
                "function {} has duplicate param {param}",
                raw.name
            )));
        }
    }
    let instructions = raw
        .instructions
        .iter()
        .map(parse_instruction)
        .collect::<Result<Vec<_>, _>>()?;
    if instructions.is_empty() {
        return Err(BytecodeError::InvalidProgram(format!(
            "function {} must have instructions",
            raw.name
        )));
    }
    Ok(FunctionBytecode {
        name: raw.name,
        instructions,
        params: raw.params,
    })
}

pub fn decode_program_json(text: &str) -> Result<BytecodeProgram, BytecodeError> {
    let raw: RawProgram = serde_json::from_str(text)?;
    decode_raw_program(raw)
}

pub fn decode_conformance_fixture(text: &str) -> Result<(BytecodeProgram, ConformanceFixture), BytecodeError> {
    let fixture: ConformanceFixture = serde_json::from_str(text)?;
    let program = decode_raw_program(RawProgram {
        version: fixture.version,
        instructions: fixture.instructions.clone(),
        functions: fixture.functions.clone(),
        modules: fixture.modules.clone(),
    })?;
    Ok((program, fixture))
}

fn decode_raw_program(raw: RawProgram) -> Result<BytecodeProgram, BytecodeError> {
    if raw.version != 1 && raw.version != 2 {
        return Err(BytecodeError::UnsupportedVersion(raw.version));
    }
    if raw.instructions.is_empty() {
        return Err(BytecodeError::InvalidProgram(
            "instructions must be non-empty".into(),
        ));
    }
    let instructions = raw
        .instructions
        .iter()
        .map(parse_instruction)
        .collect::<Result<Vec<_>, _>>()?;
    let functions = raw
        .functions
        .into_iter()
        .map(parse_function)
        .collect::<Result<Vec<_>, _>>()?;
    let modules = raw
        .modules
        .into_iter()
        .map(|module| {
            let functions = module
                .functions
                .into_iter()
                .map(parse_function)
                .collect::<Result<Vec<_>, _>>()?;
            Ok(ModuleBytecode {
                name: module.name,
                functions,
            })
        })
        .collect::<Result<Vec<_>, _>>()?;
    Ok(BytecodeProgram {
        version: raw.version,
        instructions,
        functions,
        modules,
    })
}

pub fn resolve_call_target<'a>(
    program: &'a BytecodeProgram,
    target: &str,
) -> Result<&'a FunctionBytecode, BytecodeError> {
    if let Some((module_name, fn_name)) = target.split_once('.') {
        for module in &program.modules {
            if module.name == module_name {
                for function in &module.functions {
                    if function.name == fn_name || function.name == target {
                        return Ok(function);
                    }
                }
            }
        }
        return Err(BytecodeError::InvalidProgram(format!(
            "unknown module function {target:?}"
        )));
    }
    for function in &program.functions {
        if function.name == target {
            return Ok(function);
        }
    }
    Err(BytecodeError::InvalidProgram(format!(
        "unknown function {target:?}"
    )))
}
