use crate::bytecode::{
    BytecodeError, BytecodeProgram, Instruction, OpCode, Operand, resolve_call_target,
};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Value {
    Int(i64),
    Text(String),
}

impl Value {
    fn as_output(&self) -> String {
        match self {
            Self::Int(value) => value.to_string(),
            Self::Text(value) => value.clone(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VmError {
    pub message: String,
}

impl VmError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

struct CallFrame {
    return_ip: usize,
    instructions: Vec<Instruction>,
    locals_snapshot: HashMap<String, Value>,
}

pub struct SanskriptVm {
    pub globals: HashMap<String, Value>,
    pub locals: HashMap<String, Value>,
    pub output: Vec<String>,
    stack: Vec<Value>,
    program: Option<BytecodeProgram>,
    instructions: Vec<Instruction>,
    call_stack: Vec<CallFrame>,
}

impl Default for SanskriptVm {
    fn default() -> Self {
        Self::new()
    }
}

impl SanskriptVm {
    pub fn new() -> Self {
        Self {
            globals: HashMap::new(),
            locals: HashMap::new(),
            output: Vec::new(),
            stack: Vec::new(),
            program: None,
            instructions: Vec::new(),
            call_stack: Vec::new(),
        }
    }

    pub fn execute(&mut self, program: BytecodeProgram) -> Result<Vec<String>, VmError> {
        self.globals.clear();
        self.locals.clear();
        self.output.clear();
        self.stack.clear();
        self.call_stack.clear();
        self.instructions = program.instructions.clone();
        self.program = Some(program);
        self.run(0)?;
        Ok(self.output.clone())
    }

    fn run(&mut self, start_ip: usize) -> Result<(), VmError> {
        let mut ip = start_ip;
        while ip < self.instructions.len() {
            let instruction = self.instructions[ip].clone();
            if instruction.opcode == OpCode::Halt {
                if let Some(frame) = self.call_stack.pop() {
                    self.instructions = frame.instructions;
                    self.locals = frame.locals_snapshot;
                    ip = frame.return_ip;
                    continue;
                }
                break;
            }
            let next_ip = self.execute_instruction(&instruction, ip)?;
            ip = next_ip.unwrap_or(ip + 1);
        }
        Ok(())
    }

    fn execute_instruction(
        &mut self,
        instruction: &Instruction,
        ip: usize,
    ) -> Result<Option<usize>, VmError> {
        match instruction.opcode {
            OpCode::PushInt => {
                let value = self.expect_int(instruction)?;
                self.stack.push(Value::Int(value));
                Ok(None)
            }
            OpCode::PushText => {
                let value = self.expect_text(instruction)?;
                self.stack.push(Value::Text(value));
                Ok(None)
            }
            OpCode::LoadName => {
                let name = self.expect_name(instruction)?;
                self.stack.push(self.lookup_name(&name)?);
                Ok(None)
            }
            OpCode::StoreName => {
                let name = self.expect_name(instruction)?;
                let value = self.pop()?;
                self.store_name(name, value);
                Ok(None)
            }
            OpCode::Add => {
                let right = self.pop_int()?;
                let left = self.pop_int()?;
                self.stack.push(Value::Int(left + right));
                Ok(None)
            }
            OpCode::Subtract => {
                let right = self.pop_int()?;
                let left = self.pop_int()?;
                self.stack.push(Value::Int(left - right));
                Ok(None)
            }
            OpCode::Multiply => {
                let right = self.pop_int()?;
                let left = self.pop_int()?;
                self.stack.push(Value::Int(left * right));
                Ok(None)
            }
            OpCode::Divide => {
                let right = self.pop_int()?;
                if right == 0 {
                    return Err(VmError::new("Division by zero"));
                }
                let left = self.pop_int()?;
                self.stack.push(Value::Int(left / right));
                Ok(None)
            }
            OpCode::CompareEq => {
                let right = self.pop()?;
                let left = self.pop()?;
                self.stack.push(Value::Int(if left == right { 1 } else { 0 }));
                Ok(None)
            }
            OpCode::CompareLt => {
                let right = self.pop_int()?;
                let left = self.pop_int()?;
                self.stack.push(Value::Int(if left < right { 1 } else { 0 }));
                Ok(None)
            }
            OpCode::Emit => {
                let value = self.pop()?;
                self.output.push(value.as_output());
                Ok(None)
            }
            OpCode::Jump => Ok(Some(self.expect_int(instruction)? as usize)),
            OpCode::JumpIfZero => {
                let value = self.pop_int()?;
                if value == 0 {
                    Ok(Some(self.expect_int(instruction)? as usize))
                } else {
                    Ok(None)
                }
            }
            OpCode::Call => {
                let target = self.expect_name(instruction)?;
                let program = self.program.as_ref().ok_or_else(|| {
                    VmError::new("CALL requires a full BytecodeProgram context")
                })?;
                let function = resolve_call_target(program, &target)
                    .map_err(|err| VmError::new(err.to_string()))?
                    .clone();
                let mut args = Vec::new();
                for _ in &function.params {
                    args.push(self.pop()?);
                }
                args.reverse();
                let locals = function
                    .params
                    .iter()
                    .cloned()
                    .zip(args.into_iter())
                    .collect::<HashMap<_, _>>();
                self.call_stack.push(CallFrame {
                    return_ip: ip + 1,
                    instructions: self.instructions.clone(),
                    locals_snapshot: self.locals.clone(),
                });
                self.locals = locals;
                self.instructions = function.instructions;
                Ok(Some(0))
            }
            OpCode::Return => {
                let value = self.pop()?;
                let frame = self
                    .call_stack
                    .pop()
                    .ok_or_else(|| VmError::new("RETURN outside of a function call"))?;
                self.instructions = frame.instructions;
                self.locals = frame.locals_snapshot;
                self.stack.push(value);
                Ok(Some(frame.return_ip))
            }
            OpCode::Pop => {
                self.pop()?;
                Ok(None)
            }
            OpCode::Halt => Ok(None),
        }
    }

    fn lookup_name(&self, name: &str) -> Result<Value, VmError> {
        if let Some(value) = self.locals.get(name) {
            return Ok(value.clone());
        }
        self.globals
            .get(name)
            .cloned()
            .ok_or_else(|| VmError::new(format!("Unknown stored value: {name:?}")))
    }

    fn store_name(&mut self, name: String, value: Value) {
        if self.locals.contains_key(&name) {
            self.locals.insert(name, value);
        } else {
            self.globals.insert(name, value);
        }
    }

    fn pop(&mut self) -> Result<Value, VmError> {
        self.stack
            .pop()
            .ok_or_else(|| VmError::new("Sanskript VM stack underflow"))
    }

    fn pop_int(&mut self) -> Result<i64, VmError> {
        match self.pop()? {
            Value::Int(value) => Ok(value),
            Value::Text(value) => Err(VmError::new(format!(
                "Expected integer stack value, got {value:?}"
            ))),
        }
    }

    fn expect_int(&self, instruction: &Instruction) -> Result<i64, VmError> {
        match &instruction.operand {
            Some(Operand::Int(value)) => Ok(*value),
            _ => Err(VmError::new(format!(
                "{:?} expected an integer operand",
                instruction.opcode
            ))),
        }
    }

    fn expect_name(&self, instruction: &Instruction) -> Result<String, VmError> {
        match &instruction.operand {
            Some(Operand::Name(value)) => Ok(value.clone()),
            _ => Err(VmError::new(format!(
                "{:?} expected a name operand",
                instruction.opcode
            ))),
        }
    }

    fn expect_text(&self, instruction: &Instruction) -> Result<String, VmError> {
        match &instruction.operand {
            Some(Operand::Text(value)) => Ok(value.clone()),
            _ => Err(VmError::new(format!(
                "{:?} expected a text operand",
                instruction.opcode
            ))),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::bytecode::decode_program_json;

    #[test]
    fn runs_v1_assign_increment_fixture() {
        let text = include_str!("../../data/bytecode/conformance/assign_increment_emit.json");
        let program = decode_program_json(text).expect("decode");
        let mut vm = SanskriptVm::new();
        let output = vm.execute(program).expect("execute");
        assert_eq!(output, vec!["7".to_string()]);
        assert_eq!(vm.globals.get("phala"), Some(&Value::Int(7)));
    }
}
