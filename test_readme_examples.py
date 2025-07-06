#!/usr/bin/env python3
"""Test CodeCanopy according to README examples."""

import os
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path


def create_test_project():
    """Create a comprehensive test project structure matching README examples."""
    test_dir = Path(tempfile.mkdtemp(prefix="codecanopy_readme_test_"))
    
    # Create React-like project structure
    (test_dir / "src").mkdir()
    (test_dir / "src" / "components").mkdir()
    (test_dir / "src" / "hooks").mkdir()
    (test_dir / "src" / "utils").mkdir()
    (test_dir / "src" / "auth").mkdir()
    (test_dir / "src" / "middleware").mkdir()
    (test_dir / "tests").mkdir()
    (test_dir / "tests" / "unit").mkdir()
    (test_dir / "tests" / "integration").mkdir()
    (test_dir / "docs").mkdir()
    (test_dir / "node_modules").mkdir()
    (test_dir / "dist").mkdir()
    (test_dir / "build").mkdir()
    (test_dir / "coverage").mkdir()
    
    # Create files
    files = {
        # React components
        "src/components/Header.js": """import React from 'react';

const Header = ({ title }) => {
  return <h1>{title}</h1>;
};

export default Header;""",
        
        "src/components/Footer.js": """import React from 'react';

const Footer = () => {
  return <footer>© 2024 My App</footer>;
};

export default Footer;""",
        
        "src/components/Navigation.js": """import React from 'react';

const Navigation = () => {
  return <nav>Navigation</nav>;
};

export default Navigation;""",
        
        # Hooks
        "src/hooks/useAuth.js": """import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // Auth logic here
  }, []);
  
  return { user, setUser };
};""",
        
        # Utils
        "src/utils/api.js": """export const fetchUser = async (id) => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};

export const fetchPosts = async () => {
  const response = await fetch('/api/posts');
  return response.json();
};""",
        
        "src/utils/helpers.js": """export const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

export const capitalize = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};""",
        
        # Auth
        "src/auth/login.js": """export const login = async (credentials) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return response.json();
};""",
        
        # Middleware
        "src/middleware/auth.js": """export const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  next();
};""",
        
        # Main files
        "src/index.js": """import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));""",
        
        "src/App.js": """import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {
  return (
    <div>
      <Header title="My App" />
      <main>Content here</main>
      <Footer />
    </div>
  );
};

export default App;""",
        
        # Test files
        "tests/unit/Header.test.js": """import { render } from '@testing-library/react';
import Header from '../../src/components/Header';

test('Header renders title', () => {
  const { getByText } = render(<Header title="Test" />);
  expect(getByText('Test')).toBeInTheDocument();
});""",
        
        "tests/integration/api.test.js": """import { fetchUser } from '../../src/utils/api';

test('fetchUser returns user data', async () => {
  const user = await fetchUser(1);
  expect(user).toBeDefined();
});""",
        
        # Config files
        "package.json": '{"name": "test-project", "version": "1.0.0"}',
        "README.md": "# Test Project\n\nThis is a test project for CodeCanopy.",
        
        # Files to be ignored
        "node_modules/some-package/index.js": "module.exports = {};",
        "dist/bundle.js": "console.log('bundled');",
        "build/index.html": "<html><body>Built</body></html>",
        "coverage/lcov.info": "SF:src/index.js",
        
        # Large file to test size limits
        "src/large-file.js": "// " + "x" * 50000,  # 50KB file
    }
    
    for file_path, content in files.items():
        full_path = test_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    return test_dir


def run_codecanopy_command(cmd, cwd=None):
    """Run a codecanopy command and return the output."""
    try:
        result = subprocess.run(
            ["python", "-m", "codecanopy"] + cmd.split(),
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def test_tree_examples():
    """Test tree command examples from README."""
    print("Testing tree command examples...")
    
    test_dir = create_test_project()
    
    try:
        # Test 1: Basic tree with focus
        print("\n1. Testing: codecanopy tree --focus src --ignore node_modules,dist")
        stdout, stderr, code = run_codecanopy_command("tree --focus src --ignore node_modules,dist", cwd=test_dir)
        
        if code == 0:
            assert "src/" in stdout, "src/ should be in output"
            assert "components/" in stdout, "components/ should be in output"
            assert "node_modules" not in stdout, "node_modules should be ignored"
            assert "dist" not in stdout, "dist should be ignored"
            print("✓ Basic tree with focus works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 2: Multiple focused directories
        print("\n2. Testing: codecanopy tree --focus src/components,src/hooks --depth 2")
        stdout, stderr, code = run_codecanopy_command("tree --focus src/components,src/hooks --depth 2", cwd=test_dir)
        
        if code == 0:
            assert "src/" in stdout, "src/ should be in output"
            assert "components/" in stdout, "components/ should be in output"
            assert "hooks/" in stdout, "hooks/ should be in output"
            print("✓ Multiple focused directories work")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 3: Show files
        print("\n3. Testing: codecanopy tree --files --focus src")
        stdout, stderr, code = run_codecanopy_command("tree --files --focus src", cwd=test_dir)
        
        if code == 0:
            assert "Header.js" in stdout, "Header.js should be shown"
            assert "Footer.js" in stdout, "Footer.js should be shown"
            print("✓ Show files works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 4: Custom depth
        print("\n4. Testing: codecanopy tree --depth 1")
        stdout, stderr, code = run_codecanopy_command("tree --depth 1", cwd=test_dir)
        
        if code == 0:
            assert "src/" in stdout, "src/ should be in output"
            # Should not show deep files
            assert "Header.js" not in stdout, "Header.js should not be shown at depth 1"
            print("✓ Custom depth works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        return True
        
    finally:
        shutil.rmtree(test_dir)


def test_cat_examples():
    """Test cat command examples from README."""
    print("\nTesting cat command examples...")
    
    test_dir = create_test_project()
    
    try:
        # Test 1: All JavaScript files
        print("\n1. Testing: codecanopy cat 'src/**/*.js'")
        stdout, stderr, code = run_codecanopy_command("cat 'src/**/*.js'", cwd=test_dir)
        
        if code == 0:
            assert "Header.js" in stdout, "Header.js should be in output"
            assert "Footer.js" in stdout, "Footer.js should be in output"
            assert "App.js" in stdout, "App.js should be in output"
            assert "const Header" in stdout, "Header component should be in output"
            print("✓ All JavaScript files work")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 2: Exclude test files
        print("\n2. Testing: codecanopy cat 'src/**/*.js' --exclude '**/*.test.js'")
        stdout, stderr, code = run_codecanopy_command("cat 'src/**/*.js' --exclude '**/*.test.js'", cwd=test_dir)
        
        if code == 0:
            assert "Header.js" in stdout, "Header.js should be in output"
            assert "Header.test.js" not in stdout, "Header.test.js should be excluded"
            print("✓ Exclude patterns work")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 3: Custom headers
        print("\n3. Testing: codecanopy cat 'src/index.js' --header '// File: {path}'")
        stdout, stderr, code = run_codecanopy_command("cat 'src/index.js' --header '// File: {path}'", cwd=test_dir)
        
        if code == 0:
            assert "// File: src/index.js" in stdout, "Custom header should be present"
            assert "ReactDOM.render" in stdout, "File content should be present"
            print("✓ Custom headers work")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test 4: Size limits
        print("\n4. Testing: codecanopy cat 'src/**/*.js' --max-size 1KB")
        stdout, stderr, code = run_codecanopy_command("cat 'src/**/*.js' --max-size 1KB", cwd=test_dir)
        
        if code == 0:
            assert "large-file.js" not in stdout, "Large file should be skipped"
            assert "Header.js" in stdout, "Small files should still be included"
            print("✓ Size limits work")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        return True
        
    finally:
        shutil.rmtree(test_dir)


def test_config_examples():
    """Test configuration examples from README."""
    print("\nTesting configuration examples...")
    
    test_dir = create_test_project()
    
    try:
        # Create config file
        config_content = {
            "ignore": ["node_modules", "dist", "build"],
            "default_depth": 2,
            "header_format": "--- {path} ---",
            "max_file_size": "10KB",
            "focus_dirs": ["src"]
        }
        
        config_file = test_dir / ".codecanopy.json"
        import json
        config_file.write_text(json.dumps(config_content))
        
        # Test config loading
        print("\n1. Testing config file loading")
        stdout, stderr, code = run_codecanopy_command("tree", cwd=test_dir)
        
        if code == 0:
            assert "src/" in stdout, "src/ should be in output"
            assert "node_modules" not in stdout, "node_modules should be ignored"
            assert "dist" not in stdout, "dist should be ignored"
            print("✓ Config file loading works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Test custom header format
        print("\n2. Testing custom header format")
        stdout, stderr, code = run_codecanopy_command("cat 'src/index.js'", cwd=test_dir)
        
        if code == 0:
            assert "--- src/index.js ---" in stdout, "Custom header format should be used"
            print("✓ Custom header format works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        return True
        
    finally:
        shutil.rmtree(test_dir)


def test_real_world_examples():
    """Test real-world examples from README."""
    print("\nTesting real-world examples...")
    
    test_dir = create_test_project()
    
    try:
        # Frontend React Project example
        print("\n1. Testing Frontend React Project example")
        stdout, stderr, code = run_codecanopy_command(
            "tree --focus src/components,src/hooks --depth 2", 
            cwd=test_dir
        )
        
        if code == 0:
            assert "components/" in stdout, "components/ should be focused"
            assert "hooks/" in stdout, "hooks/ should be focused"
            print("✓ Frontend React Project example works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        # Component code for LLM review
        print("\n2. Testing component code for LLM review")
        stdout, stderr, code = run_codecanopy_command(
            "cat 'src/components/**/*.js' --exclude '**/*.test.*'", 
            cwd=test_dir
        )
        
        if code == 0:
            assert "Header.js" in stdout, "Header.js should be included"
            assert "Footer.js" in stdout, "Footer.js should be included"
            assert "Header.test.js" not in stdout, "Test files should be excluded"
            print("✓ Component code for LLM review works")
        else:
            print(f"❌ Command failed: {stderr}")
            return False
        
        return True
        
    finally:
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    print("Running CodeCanopy README Examples Tests...\n")
    
    all_passed = True
    
    try:
        all_passed &= test_tree_examples()
        all_passed &= test_cat_examples()
        all_passed &= test_config_examples()
        all_passed &= test_real_world_examples()
        
        if all_passed:
            print("\n✅ All README examples work correctly!")
            print("🎉 CodeCanopy is working as advertised in the README!")
        else:
            print("\n❌ Some README examples failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 