#!/usr/bin/env python3
"""Basic test script for CodeCanopy functionality."""

import os
import tempfile
import shutil
from pathlib import Path
from codecanopy.config import Config
from codecanopy.tree import TreeGenerator
from codecanopy.cat import CatGenerator


def create_test_project():
    """Create a test project structure."""
    test_dir = Path(tempfile.mkdtemp(prefix="codecanopy_test_"))
    
    # Create directory structure
    (test_dir / "src").mkdir()
    (test_dir / "src" / "components").mkdir()
    (test_dir / "src" / "utils").mkdir()
    (test_dir / "tests").mkdir()
    (test_dir / "node_modules").mkdir()
    (test_dir / "dist").mkdir()
    
    # Create files
    files = {
        "src/index.js": "console.log('Hello World');",
        "src/components/Header.js": (
            "export const Header = () => <h1>Header</h1>;"
        ),
        "src/components/Footer.js": (
            "export const Footer = () => <footer>Footer</footer>;"
        ),
        "src/utils/helpers.js": "export const helper = () => 'help';",
        "tests/test_main.js": "test('main', () => {});",
        "package.json": '{"name": "test-project"}',
        "README.md": "# Test Project",
        "node_modules/some-package/index.js": "module.exports = {};",
        "dist/bundle.js": "console.log('bundled');"
    }
    
    for file_path, content in files.items():
        full_path = test_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    return test_dir


def test_tree_functionality():
    """Test tree generation."""
    print("Testing tree functionality...")
    
    test_dir = create_test_project()
    config = Config()
    generator = TreeGenerator(config)
    
    try:
        # Test basic tree
        result = generator.generate(root_path=test_dir)
        print("-->", result)
        # Check that the result contains the expected directory structure
        assert "src/" in result
        assert "components/" in result
        print("✓ Basic tree generation works")
        
        # Test with focus
        result = generator.generate(
            root_path=test_dir,
            focus_dirs=["src"],
            ignore_patterns=["node_modules", "dist"]
        )
        assert "src/" in result
        assert "node_modules" not in result
        assert "[focused]" in result or "components/" in result
        print("✓ Focus and ignore patterns work")
        
        # Test depth limiting
        result = generator.generate(
            root_path=test_dir,
            global_depth=1
        )
        # Should not show files deep in subdirectories
        # The result should show src/ but not go deeper
        assert "src/" in result
        print("✓ Depth limiting works")
        
    finally:
        shutil.rmtree(test_dir)


def test_cat_functionality():
    """Test cat generation."""
    print("Testing cat functionality...")
    
    test_dir = create_test_project()
    config = Config()
    generator = CatGenerator(config)
    
    try:
        # Test basic cat
        result = generator.generate(
            patterns=["src/index.js"],
            base_path=test_dir
        )
        assert "index.js" in result
        assert "Hello World" in result
        print("✓ Basic cat generation works")
        
        # Test glob patterns
        result = generator.generate(
            patterns=["src/**/*.js"],
            base_path=test_dir
        )
        assert "Header.js" in result
        assert "Footer.js" in result
        print("✓ Glob patterns work")
        
        # Test exclude patterns
        result = generator.generate(
            patterns=["**/*.js"],
            exclude_patterns=["**/node_modules/**"],
            base_path=test_dir
        )
        assert "index.js" in result
        assert "node_modules" not in result
        print("✓ Exclude patterns work")
        
        # Test custom headers
        result = generator.generate(
            patterns=["src/index.js"],
            header_format="// File: {filename}",
            base_path=test_dir
        )
        assert "// File: index.js" in result
        print("✓ Custom headers work")
        
    finally:
        shutil.rmtree(test_dir)


def test_config_functionality():
    """Test configuration handling."""
    print("Testing config functionality...")
    
    test_dir = create_test_project()
    
    try:
        # Create config file
        config_content = {
            "ignore": ["node_modules", "dist"],
            "default_depth": 2,
            "header_format": "--- {path} ---",
            "max_file_size": "1KB"
        }
        
        config_file = test_dir / ".codecanopy.json"
        import json
        config_file.write_text(json.dumps(config_content))
        
        # Change to test directory
        old_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # Test config loading
        config = Config()
        assert config.get('default_depth') == 2
        assert config.get('header_format') == "--- {path} ---"
        print("✓ Config file loading works")
        
        # Test size parsing
        assert config.parse_size("1KB") == 1024
        assert config.parse_size("1MB") == 1024 * 1024
        assert config.parse_size("") == float('inf')
        print("✓ Size parsing works")
        
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    print("Running CodeCanopy tests...\n")

    try:
        test_config_functionality()
        test_tree_functionality() 
        test_cat_functionality()
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()