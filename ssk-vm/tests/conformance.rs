use ssk_vm::{SanskriptVm, decode_conformance_fixture};
use std::fs;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

fn conformance_dir() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("..")
        .join("data")
        .join("bytecode")
        .join("conformance")
}

#[test]
fn all_json_conformance_fixtures_match_python_contract() {
    let root = conformance_dir();
    assert!(root.is_dir(), "missing conformance dir at {}", root.display());

    for entry in WalkDir::new(&root).into_iter().map(|e| e.expect("walkdir")) {
        let path = entry.path();
        if path.extension().and_then(|ext| ext.to_str()) != Some("json") {
            continue;
        }
        let text = fs::read_to_string(path).expect("read fixture");
        let (program, fixture) = decode_conformance_fixture(&text).expect("decode fixture");
        let mut vm = SanskriptVm::new();
        let output = vm.execute(program).expect("execute fixture");
        assert_eq!(
            output, fixture.expected_output,
            "output mismatch in {}",
            path.display()
        );
        for (name, expected) in &fixture.expected_environment {
            assert_eq!(
                vm.globals.get(name),
                Some(expected),
                "environment mismatch for {name} in {}",
                path.display()
            );
        }
    }
}
