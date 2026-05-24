use ssk_vm::{SanskriptVm, decode_conformance_fixture, decode_program_json};
use std::env;
use std::fs;
use std::process;

fn main() {
    let path = match env::args().nth(1) {
        Some(path) => path,
        None => {
            eprintln!("usage: ssk-vm <bytecode.json>");
            process::exit(2);
        }
    };

    let text = fs::read_to_string(&path).unwrap_or_else(|err| {
        eprintln!("failed to read {path}: {err}");
        process::exit(1);
    });

    let mut vm = SanskriptVm::new();
    if text.contains("\"expected_output\"") {
        let (program, fixture) = decode_conformance_fixture(&text).unwrap_or_else(|err| {
            eprintln!("decode error: {err}");
            process::exit(1);
        });
        let output = vm.execute(program).unwrap_or_else(|err| {
            eprintln!("runtime error: {}", err.message);
            process::exit(1);
        });
        if output != fixture.expected_output {
            eprintln!("output mismatch: expected {:?}, got {:?}", fixture.expected_output, output);
            process::exit(1);
        }
        for (name, expected) in &fixture.expected_environment {
            let actual = vm.globals.get(name);
            if actual != Some(expected) {
                eprintln!(
                    "environment mismatch for {name}: expected {expected}, got {actual:?}"
                );
                process::exit(1);
            }
        }
        for line in &output {
            println!("{line}");
        }
        return;
    }

    let program = decode_program_json(&text).unwrap_or_else(|err| {
        eprintln!("decode error: {err}");
        process::exit(1);
    });
    let output = vm.execute(program).unwrap_or_else(|err| {
        eprintln!("runtime error: {}", err.message);
        process::exit(1);
    });
    for line in output {
        println!("{line}");
    }
}
