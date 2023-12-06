<!-- TOC -->
  * [Test Introduction](#test-introduction)
  * [Test_methods Class](#testmethods-class)
    * [`assertEqual(a, b)`](#assertequala-b)
    * [`assertIsNone(value)`](#assertisnonevalue)
    * [`assertFalse(condition)`](#assertfalsecondition)
    * [`assertTrue(condition)`](#asserttruecondition)
    * [`setUp()`](#setup)
    * [`tearDown()`](#teardown)
  * [TestFileOperations Class](#testfileoperations-class)
  * [Test 1. read_file( )](#test-1-readfile-)
    * ['test_read_success_to_existing'](#testreadsuccesstoexisting)
      * [Overview:](#overview)
      * [Implementation Details:](#implementation-details)
      * [Conclusion:](#conclusion)
    * ['test_read_none_to_non_existing'](#testreadnonetononexisting)
      * [Overview:](#overview-1)
      * [Implementation Details:](#implementation-details-1)
      * [Conclusion:](#conclusion-1)
    * ['test_read_fail'](#testreadfail)
      * [Overview:](#overview-2)
      * [Implementation Details:](#implementation-details-2)
      * [Conclusion:](#conclusion-2)
  * [Test 2. create_file()](#test-2-createfile)
    * ['test_create_success'](#testcreatesuccess)
      * [Overview:](#overview-3)
      * [Implementation Details:](#implementation-details-3)
      * [Conclusion:](#conclusion-3)
    * ['test_create_fail'](#testcreatefail)
      * [Overview:](#overview-4)
      * [Implementation Details:](#implementation-details-4)
      * [Conclusion:](#conclusion-4)
  * [Test 3: `write_file()`](#test-3-writefile)
    * [`test_write_success_to_existing_file`](#testwritesuccesstoexistingfile)
      * [Overview:](#overview-5)
      * [Implementation Details:](#implementation-details-5)
      * [Conclusion:](#conclusion-5)
    * [`test_write_fail_to_invalid_path`](#testwritefailtoinvalidpath)
      * [Overview:](#overview-6)
      * [Implementation Details:](#implementation-details-6)
      * [Conclusion:](#conclusion-6)
    * [`test_write_fail_with_no_permission`](#testwritefailwithnopermission)
      * [Overview:](#overview-7)
      * [Implementation Details:](#implementation-details-7)
      * [Conclusion:](#conclusion-7)
  * [Test 4. delete_file()](#test-4-deletefile)
    * [`test_delete_success`](#testdeletesuccess)
      * [Overview:](#overview-8)
      * [Implementation Details:](#implementation-details-8)
      * [Conclusion:](#conclusion-8)
    * [`test_delete_fail_path`](#testdeletefailpath)
      * [Overview:](#overview-9)
      * [Implementation Details:](#implementation-details-9)
      * [Conclusion:](#conclusion-9)
    * [`test_delete_fail_no_permission`](#testdeletefailnopermission)
      * [Overview:](#overview-10)
      * [Implementation Details:](#implementation-details-10)
      * [Conclusion:](#conclusion-10)
  * [Test_runners Class](#testrunners-class)
  * [Summary](#summary)
<!-- TOC -->
---
## Test Introduction
The `run_tests.py` file includes 11 tests implemented in the MacOS system to test the functions read_file( ),create_file( ), write_file( ), and delete_file( ). There are difference in both implementation and execution on Windows machines in case of folder permission using `os.chmod` for simulation.The file path are different when executed by the run button in the code editor(VsCode) versus when run using command line execution.

 The code is structured around three main classes:

- Test_methods: Because we are not allowed to use any framework, for less duplicate codes we design this class which provides methods for performing common test assertions, such as checking equality, verifying if a value is None, and validating conditions. It includes setup and cleanup methods for managing the test environment.

- TestFileOperations: This class inherits from 'Test_methods' and defines test methods for various file operations. It includes test cases for reading, creating, writing, and deleting files in different scenarios.

- Test_runners: This class enables the execution of test methods from the 'TestFileOperations' class. It allows users to select specific tests to run based on matching a pattern in the name of the test. The 'run_tests' method runs the selected tests and generates a summary of test results, including the number of tests passed, failed, and errors.

To avoid code duplication and make our code more maintainable, we define the file paths and names globally.

The script uses Python's argparse module to accept command-line arguments, allowing users to specify which tests to run. The `"__name__ == "__main__":` block at the end ensures that the test suite is executed when the script is run directly.


---

## Test_methods Class

This section introduces commonly used tests methods during our tasks.

### `assertEqual(a, b)`
Verifies if the two provided arguments, `a` and `b`, are equal.

```python
    def assertEqual(self, a, b):
        if a != b:
            raise AssertionError(f"Assertion failed: Expected {a} to equal {b}, but they are different.")
```

### `assertIsNone(value)`
Verifies if the provided value is None.

```python
    def assertIsNone(self, value):
        if value is not None:
            raise AssertionError(f"Assertion failed: Expected the value to be None, but got {type(value).__name__} with value {value}.")
```

### `assertFalse(condition)`
Verifies if the given condition is False.

```python
    def assertFalse(self, condition):
        if condition is not False:
            raise AssertionError(f"Assertion failed: Expected the condition to be False, but got {type(condition).__name__} with value {condition}.")
```

### `assertTrue(condition)`
Verifies if the given condition is True.

```python
    def assertTrue(self, condition):
        if not condition:
            raise AssertionError(f"Assertion failed: Expected the condition to be True, but it evaluated to False.")

```

### `setUp()`
Setup method to initialize the list need to be removed after testing

```python
def setUp(self):
    self.files_to_remove = []
    # To ensure the __pycache__ can be rermoved after test
    self.files_to_remove.append( "__pycache__")
```

### `tearDown()`
To remove any created files during testing, it can clear all files or directories under the path.

```python
    def tearDown(self):
        for path in self.files_to_remove:
            full_path = os.path.join(valid_file_path, path)
            if os.path.exists(full_path):

                # Delete the files
                if os.path.isfile(full_path):
                    os.remove(full_path)
                # Delete the folder
                elif os.path.isdir(full_path):
                    #print(full_path)
                    shutil.rmtree(full_path)
```
---

## TestFileOperations Class

## Test 1. read_file( )
### 'test_read_success_to_existing'
#### Overview:
This test assesses the behavior of the read_file function when it successfully reads the content of an existing file, so as to test 1st branch.

#### Implementation Details:
1. **Setup:**
    - To create a suitable environment for the test, an existing file named 'Existingfilename.txt' is created within the 'valid_file_path'.
    - This file is filled with a sample content to ensure there is data to be read.
    - The file's name is added to the files_to_remove list for proper cleanup during the test teardown phase

2. **Test Execution:**
    - The test is performed by calling the read_file function with the name of the existing file  as the argument.
    - The content read from the file is stored in the read_content variable.
    - An assertion checks whether the content is equal to the expected content.

3. **Teardown:**
    - The super( ).tearDown( ) method is invoked to ensure that temporary files created during the test setup are removed, leaving the testing environment in a clean state.
#### Conclusion:
By successfully reading the content of an existing file with known content, this test confirms that the read_file function can correctly retrieve and return the content from a valid file location, so the 1st branch has been successfully tested.

***

### 'test_read_none_to_non_existing'
#### Overview:
This test evaluates the behavior of the read_file function when attempting to read the content from a non-existing file. It ensures that the function correctly returns None when dealing with a file that does not exist at the specified location, so as to test 2nd branch.

#### Implementation Details:
1. **Setup:**
    - The setup phase constructs the enviroment with the correct path , but with incorrect filename while another valid file exists inside the path. This mimics the situation where a specified file does not exist in a particular folder.
    
2. **Test Execution:**
    - The read_file function is called with the 'Nonexistingfilename', and the result should  be None.

3. **Teardown:**
The super().tearDown() method is invoked to clean up temporary files created during the test setup. 
#### Conclusion:
By correctly returning None when attempting to read a file that does not exist, this test verifies that the read_file function handles non-existing files as expected, 2nd branch has been successfully tested.

***

### 'test_read_fail'
#### Overview:
This test case verifies the behavior of the read_file function when attempting to read a file for which the user lacks read permissions, so as to test 3rd branch.

#### Implementation Details:
1. **Setup:**
    - A folder named "no_read_permission_folder" is created in the valid_file_path, and within this folder, valid file(s) would be created.
    - Read permissions for the folder, "no_read_permission_folder" is removed (0o222) to simulate a situation where a file inside it cannot be read.



2. **Test Execution:**
    - The read_file function is called with the path to the file "Existingfilename.txt" to test its behavior when reading a file without read permissions.
    - The test asserts that the result returned by the read_file function is None.

3. **Teardown:**
In the teardown phase, the testing environment is cleaned up. 
#### Conclusion:
The test has passed, demonstrating that the read_file function correctly returns None also an error message when trying to read a file without read permissions, 3rd branch has been successfully tested.

___

## Test 2. create_file()
### 'test_create_success'
#### Overview:
This test evaluates the behavior of the create_file function when it successfully creates a new file, so as to test 1st branch.

#### Implementation Details:
1. **Setup:**
    - The setup is mainly same as the `test_read_success`, but we do not need to simulate there actually were some pre-existing files with contents.
 

2. **Test Execution:**
    - The test attempts to create a new file using the create_file function. To ensure there is no preexisting file with the same name we verify`os.path.exists(test_file_name) `returns false
    - The successful creation of the file is confirmed by asserting that `create_file(test_file_name, content=content)` returns True
    - Furthermore, the test ensures that the file indeed exists after its creation, providing an additional assertion to verify that `os.path.exists(test_file_name)` returns True.

3. **Teardown:**
In the teardown phase, we removed the newly created file from the previous step.

#### Conclusion:
This test confirms the correct behavior of the create_file function in successfully creating a new file, branch 1 has been successfully tested.

***

### 'test_create_fail'
#### Overview:
This test assesses the behavior of the create_file function when it attempts to create a file in an invalid location and fails.


#### Implementation Details:
1. **Setup:**
    - The purples of this setup is to construct an environment with an invalid path and valid filename.

2. **Test Execution:**
    - In this case, the test ensures that the create_file function correctly returns False when attempting to create a file in an invalid location(location folder doesn't actually exist). The test reconfirms that no such file is created.


3. **Teardown:**
In the teardown phase we remove the files created during test setup.
#### Conclusion:
This test affirms the proper behavior of the create_file function when it attempts to create a file in an invalid location.

***

## Test 3: `write_file()`
### `test_write_success_to_existing_file`

#### Overview:

This test case is tailored to validate the `write_file` function's capability when tasked with writing content to an already existing file, so as to test 1st branch.



#### Implementation Details:

1. **Setup:**

    - The setup is similar to the `test_read_success` case, it is used to construct an environment with create a valid file inside valid path.

   
2. **Test Execution:**

    - The test is trying to check whether the `write_file( )` can return true when it runs successfully and also to check whether the contents are written correctly by using `.read`(official way) to compare.

    
3. **Teardown:**

   The `tearDown` function cleans up the files created for the test.

#### Conclusion:

The `write_file` function returns `True` and the content extracted after execution of the function mirrors the expected content, it's evident that the function writes to files.

***


### `test_write_fail_to_invalid_path`

#### Overview:

This test checks if the `write_file` function returns false when  writing to a file at an invalid path, for testing 2nd branch.


#### Implementation Details:

1. **Setup:**

    We construct an enviroment with an invalid path and valid filename.


2. **Test Execution:**

    The function's behavior is to test whether the function can return false when the path is invalid.


3. **Teardown:**

    The `tearDown` method is then invoked to clean up files created during testing.


#### Conclusion:

The `write_file` function returns `False` for invalid paths(i.e. nonexistent folder), 2nd branch of it has been successfully tested.

***


### `test_write_fail_with_no_permission`

#### Overview:

This test evaluates the behavior of the `write_file` function when it attempts to write to a file with no write permissions, to test 2nd branch again.


#### Implementation Details:

1. **Setup:**

    - An attempt is made to create a folder named `no_write_permission_folder` inside the `valid_file_path`.
    - This folder's permissions are then altered to render it "read-only" (permissions set to `0o444`), ensuring no write operations are permissible.



2. **Test Execution:**

    - We attempt to write to a file "Existingfilename.txt" within this no-permission folder.
    - The `assertFalse` assertion confirms that the function indeed returned `False`, signaling its inability to perform the write operation.



3. **Teardown:**

    - Firstly, the permissions for the `no_write_permission_folder` are reverted back to `0o777` to ensure it's fully accessible.
    - The testing files are deleted and the folder is then subsequently removed using the `shutil.rmtree` function.



    The super class's `tearDown` method is then invoked to clean up any other potential residuals.

#### Conclusion:

The `write_file` function can't inadvertently bypass system access controls and write to an unauthorized location. The test returns False as expected, and 2nd branch has been successfully tested.

***

## Test 4. delete_file()
### `test_delete_success`
#### Overview:

The purpose of this test is to validate the `delete_file` function's capability to correctly delete files. We check if given an existing file, the function can successfully delete the file without issues.




#### Implementation Details:

1. **Setup:**

    The setup is similar to the `test_read_success`, it is used to construct an environment with a valid file inside valid path.


2. **Test Execution:**

    Use the delete_file function to delete the file.
    


3. **Teardown:**

    The `super().tearDown()` cleans the test files generated.

#### Conclusion:

This test validates the `delete_file` can successfully delete the target file, and returns True, thus 1st branch has been successfully tested.

***

### `test_delete_fail_path`

#### Overview:

This test aims to verify the behavior of the delete_file function when attempting to delete a file using a non-existent file path, so as to test 2nd branch.



#### Implementation Details:

1. **Setup:**
    - Simulate the enviroment that there is an existing file inside the path by creating a file with valid file path and valid filename.
    - Override the file path to be incorrect for next step test.


2. **Test Execution:**

    - Attempt to delete the file using the delete_file function.
    - Verify that the function cannot delete the file and returns False as the file path is incorrect.


3. **Teardown:**
  The `super().tearDown()` cleans the testing environment.

#### Conclusion:
The test_delete_fail_path test successfully verified that the delete_file function returns False when provided with an incorrect file path, 2nd branch has been successfully tested.


***

### `test_delete_fail_no_permission`

#### Overview:

This test aims to validate the behavior of the delete_file function when attempting to delete a file that resides within a folder with insufficient permissions. It checks whether the function correctly returns False, so as to test 3rd branch.


#### Implementation Details:

1. **Setup:**

    Create test files within a folder that has limited delete permissions.
    

2. **Test Execution:**

    - Attempt to delete the file using the delete_file function.
    - Verify that the function returns False as the file cannot be deleted due to insufficient permissions.

    
3. **Teardown:**

    - Restore the permissions of the folder.
    - Remove the folder and its contents, including the test files.

#### Conclusion:
The function correctly returns False when trying to delete a file within a directory with insufficient permissions, 3rd branch has been successfully tested.

---
## Test_runners Class
The 'Test_runners' class is designed to facilitate the execution and reporting of test cases. It is an extension of the TestFileOperations class.
It offers the following functionality:
  - Test Case Selection: The 'find_test' method implements `introspection` which identifies and retrieves test methods with names that start with a specified prefix. This allows us to filter tests based on a pattern.
  - Test Execution: The 'run_tests' method runs the selected test methods and records their results. It reports the status (passed, failed and error), execution time, and any reasons for failure or errors. It also provides a summary of the total test results.
  - Test Type Extraction: The 'extract_test_type' method extracts the type of test from the test method's name based on a naming convention,we get the second part of test names.
-------

## Summary
The `run_tests.py` includes 11 tests for four functions  in `file_manager.py`, these tests covers every branch of each function, and all passed. we use `setUp()` and `teardown()` for environment management, ensure every test can achieve their goals. we use `Test_runners` class  to generate detailed test report. User can use `-- select pattern` to run only the tests that contain the pattern in their name.

---


**Editors：** Arjun Roy, Weimin Yang, Zihan Liu