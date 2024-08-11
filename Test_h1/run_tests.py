import argparse 
import os
import shutil
import time
from file_manager import read_file,create_file,delete_file,write_file

# Define file paths for valid and invalid directory
valid_file_path = os.path.dirname(__file__)
invalid_file_path = os.path.join(valid_file_path, "invalid_path")
valid_file_name="Existingfilename"
invalid_file_name="Nonexistingfilename"

# Base test methods class
class Test_methods():
    # Assertion to check equality
    def assertEqual(self, a, b):
        if a != b:
            raise AssertionError(f"Assertion failed: Expected {a} to equal {b}, but they are different.")

    # Assertion to check if value is None
    def assertIsNone(self, value):
        if value is not None:
            raise AssertionError(f"Assertion failed: Expected the value to be None, but got {type(value).__name__} with value {value}.")

    # Assertion to check if condition is False
    def assertFalse(self, condition):
        if condition is not False:
            raise AssertionError(f"Assertion failed: Expected the condition to be False, but got {type(condition).__name__} with value {condition}.")

    # Assertion to check if condition is True
    def assertTrue(self, condition):
        if not condition:
            raise AssertionError(f"Assertion failed: Expected the condition to be True, but it evaluated to False.")

    
    # Setup method to initialize the list need to be removed after testing
    def setUp(self):
        self.files_to_remove = []
        # To ensure the __pycache__ could be rermoved after test
        self.files_to_remove.append( "__pycache__")
    
    # Cleanup method to remove any created files during testing, it can clear all files or directories under the path
    def tearDown(self):
        for path in self.files_to_remove:
            full_path = os.path.join(valid_file_path, path)
            if os.path.exists(full_path):  
                if os.path.isfile(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    # print(full_path)
                    shutil.rmtree(full_path)



#Main test class TestFileOperations()
#Inherit from parent class 'Test_methods'
class TestFileOperations(Test_methods):
    #define different kinds of file types for testing
    file_data = {
        'txt': "TEST CONTENT"
        # 'doc': "TEST CONTENT",
        # 'json': '{"key": "value"}',
        # 'csv': "header1,header2\nvalue1,value2",
        # 'xml': '<root><key>value</key></root>',
        # 'html': '<!DOCTYPE html><html><head><title>Title of the document</title></head><body>The content of the document......</body></html>',
        # 'md': '# Markdown Heading\nContent goes here.',
        # 'yaml': 'key: value\nanother_key: another_value',
    }


    #1. read_file() tests:
    # 1.1 Test whether the read_file function can read successfully
    def test_read_success_to_existing(self):
        # To setup the files enviroment
        def setUp(file_extension, content):
            test_file_name = f"{valid_file_name}.{file_extension}"
            
            # Create a file with the given content
            self.files_to_remove.append(test_file_name)
            test_file_name = os.path.join(valid_file_path, test_file_name)
            with open(test_file_name, 'w') as file:
                file.write(content)     
            return test_file_name

        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name = setUp(file_extension, content)

            try:
                # print(test_file_name)
                read_content = read_file(test_file_name)
                self.assertEqual(read_content, content)
            finally:
                super().tearDown()

    # 1.2 Test whether the read_file function returns None when the file does not exist
    def test_read_none_to_non_existing(self):
        def setUp(file_extension, content):

            test_file_name = f"{valid_file_name}.{file_extension}"

            
            # Create a file with the given content
            self.files_to_remove.append(test_file_name)
            with open(os.path.join(valid_file_path, test_file_name), 'w') as file:
                file.write(content)

            # overide with incorrect file name
            test_file_name=f"{invalid_file_name}.{file_extension}"
            test_file_name = os.path.join(valid_file_path, test_file_name) 
            return test_file_name
        
        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name=setUp(file_extension, content)
            # print(test_file_name)
            try:
                # Attempt to read the invalid file from the valid file path
                self.assertIsNone(read_file(test_file_name))
            finally:
                super().tearDown()

    # 1.3 Test whether the read_file function cannot read an exisiting file due to insufficient access permission
    def test_read_fail(self):

        def setUp(file_extension, content):

            # For simulating an existed file with some content in a folder with insufficient permission
            no_permission_folder = os.path.join(valid_file_path, "no_read_permission_folder")
            os.makedirs(no_permission_folder, exist_ok=True)
            test_file_name = os.path.join(no_permission_folder, valid_file_name + "."+file_extension)
            with open(test_file_name, 'w') as f:
                f.write(content)
            
            # Remove read permissions from the file so as to trigger the 3rd branch
            os.chmod(no_permission_folder, 0o222)
            
            # Add the file to the list so that it can be remover later
            self.files_to_remove.append(test_file_name)

            # Return the constructed folder to teardown function for removal
            return test_file_name, no_permission_folder
        
        def tearDown(no_permission_folder):

            # Firstly resume the permision of the folder to be removed
            os.chmod(no_permission_folder, 0o777)
            # Remove the folder
            shutil.rmtree(no_permission_folder)

        for file_extension, content in self.file_data.items():  
            super().setUp()
            test_file_name, no_permission_folder = setUp(file_extension,content) 
            # print(test_file_name)     
            try:
                # Attempt to read the file
                read_success = read_file(test_file_name)

                # Test whether read_file return None when there is an exception when we dont have permission
                self.assertIsNone(read_success)
            
            finally:
                tearDown(no_permission_folder)
                super().tearDown()




    # 2. Test create_file():
    # 2.1 Test whether the create_file function can successfully create a file with the correct contents
    def test_create_success(self):
        def setUp(file_extension,content):
            test_file_name = f"{valid_file_name}.{file_extension}"
            test_file_name = os.path.join(valid_file_path, test_file_name)
            
            # Add file to removal list
            self.files_to_remove.append(test_file_name)
            return test_file_name

        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name = setUp(file_extension,content)
            # print(test_file_name)
            try:

                # To check no previous file exists with the same file name
                self.assertFalse(os.path.exists(test_file_name))

                # Attempt to create the file by using create_file 1st branch
                self.assertTrue(create_file(test_file_name, content=content))
                
                # Assert file exists after creation
                self.assertTrue(os.path.exists(test_file_name))
            
               
            finally:
                super().tearDown()

    # 2.2 Test whether the path is incorrect to trigger the second branch of create_file
    def test_create_fail(self):
        
        def setUp(file_extension, content):

            test_file_name = f"{valid_file_name}.{file_extension}"
            
            # Create a file with the given content
            self.files_to_remove.append(test_file_name)
            with open(os.path.join(valid_file_path, test_file_name), 'w') as file:
                file.write(content)
            
            # Overide with incorrect file path
            test_file_name = os.path.join(invalid_file_path,test_file_name) 
            return test_file_name
        
        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name=setUp(file_extension, content)
            # print(test_file_name)
            try:
            
                # To confirm create_file return false when the 2nd branch is run
                self.assertFalse(create_file(test_file_name, content))

                # To confirm the invalid file path(folder) doesnt contain the file created previously
                self.assertFalse(os.path.exists(test_file_name))
            finally:
                super().tearDown()
        

    # 3. Test Writing
    # 3.1 Test write_file to successfully write to an existing file, 1st branch of the function
    def test_write_success_to_existing_file(self):

        def setUp(file_extension, content):
            test_file_name = f"{valid_file_name}.{file_extension}"
            
            # Create a file with the given content
            self.files_to_remove.append(test_file_name)
            test_file_name = os.path.join(valid_file_path, test_file_name)
            with open(test_file_name, 'w') as file:
                file.write(content)

            return test_file_name

        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name = setUp(file_extension, content)
            # print(test_file_name)
            try:

                # Test whether the function can successfully write to an existing file
                self.assertTrue(write_file(test_file_name, content))

                # Confirm the contents are consistant
                with open(test_file_name, 'r') as file:
                    content_read = file.read()

                self.assertEqual(content, content_read)

            finally:
                super().tearDown()

    # 3.2 Test to verify write_file failure due to incorrect path, test 2nd branch
    def test_write_fail_to_invalid_path(self):

        def setUp(file_extension, content):

            test_file_name = f"{valid_file_name}.{file_extension}"
            
            # Create a file with the given content
            self.files_to_remove.append(test_file_name)
            with open(os.path.join(valid_file_path, test_file_name), 'w') as file:
                file.write(content)
            
            # Overide with incorrect file path
            test_file_name = os.path.join(invalid_file_path, test_file_name) 
            return test_file_name
        
        for file_extension, content in self.file_data.items():
            super().setUp()
            test_file_name=setUp(file_extension, content)
            # print(test_file_name)
            try:

                # Verify that write is unsuccessful when the path is wrong, returns false
                write_success = write_file(test_file_name, content)
                self.assertFalse(write_success)

            finally:
                super().tearDown()




    # 3.3 Test to verify write_file failure due to insufficient write permission, test 3rd branch
    def test_write_fail_no_permission(self):
        
        def setUp(file_extension, content):

            # For simulating an existed file with some content in a folder with insufficient permission
            no_permission_folder = os.path.join(valid_file_path, "no_write_permission_folder")
            os.makedirs(no_permission_folder, exist_ok=True)
            test_file_name = os.path.join(no_permission_folder, valid_file_name +"."+ file_extension)
            with open(test_file_name, 'w') as f:
                f.write(content)
            
            # Remove write permissions from the file so that to trigger the 3rd branch
            os.chmod(no_permission_folder, 0o444)
            
            # Add the file to the list so that it can be remover later
            self.files_to_remove.append(test_file_name)

            # Return the constructed folder for teardown function to remove
            return test_file_name, no_permission_folder
        
        def tearDown(no_permission_folder):

            # Firstly resume the write permision of the folder to be removed
            os.chmod(no_permission_folder, 0o777)
            # Remove the folder
            shutil.rmtree(no_permission_folder)

        for file_extension, content in self.file_data.items():  
            super().setUp()
            test_file_name, no_permission_folder = setUp(file_extension,content)
            # print(test_file_name)
            try:
                # Verify that write is unsuccessful when there is no permission, returns false
                write_success = write_file(test_file_name, content)
                self.assertFalse(write_success)

            finally:
                tearDown(no_permission_folder)
                super().tearDown()



    # 4. Test delete_file()
    # 4.1 Test whether the function can delete the existing file successfully 
    def test_delete_success(self):

            def setUp(file_extension, content):
                test_file_name = f"{valid_file_name}.{file_extension}"
                        
                # Create a file with the given content
                self.files_to_remove.append(test_file_name)
                test_file_name = os.path.join(valid_file_path, test_file_name)
                with open(test_file_name, 'w') as file:
                    file.write(content)

                return test_file_name
            
            for file_extension, content in self.file_data.items():
                super().setUp()
                test_file_name = setUp(file_extension, content)
                # print(test_file_name)
                try:
                    # Assert file exists before deletion
                    self.assertTrue(os.path.exists(test_file_name))
                    
                    # Attempt to delete the file
                    self.assertTrue(delete_file(test_file_name))
                    
                    # Assert file does not exist after deletion
                    self.assertFalse(os.path.exists(test_file_name))
                finally:
                    super().tearDown()

    # 4.2 Test whether the function returns None when the file is not found, test branch 2
    def test_delete_fail_path(self):

            def setUp(file_extension, content):

                test_file_name = f"{valid_file_name}.{file_extension}"
                
                # Create a file with the given content
                self.files_to_remove.append(test_file_name)
                with open(os.path.join(valid_file_path, test_file_name), 'w') as file:
                    file.write(content)
                
                # Overide with incorrect file path
                test_file_name = os.path.join(invalid_file_path,test_file_name) 
                return test_file_name
            
            for file_extension, content in self.file_data.items():
                super().setUp()
                test_file_name=setUp(file_extension, content)
                # print(test_file_name)
                try:

                    # Attempt to delete the file and check whether it returns false when the file is not found
                    self.assertFalse(delete_file(test_file_name))

                finally:
                    # Remove the test files
                    super().tearDown()

    # 4.3 Test case to verify deletion failure due to insufficient permissions, test branch 3
    def test_delete_fail_no_permission(self):

        def setUp(file_extension, content):

            # For simulating an existed file with some content in a folder with insufficient permission
            no_permission_folder = os.path.join(valid_file_path, "no_delete_permission_folder")
            os.makedirs(no_permission_folder, exist_ok=True)
            test_file_name = os.path.join(no_permission_folder, valid_file_name + "." + file_extension)
            with open(test_file_name, 'w') as f:
                f.write(content)
            
            # Remove write permissions from the file so that to trigger the 3rd branch
            os.chmod(no_permission_folder, 0o444)
            
            # Add the file to the list so that it can be remover later
            self.files_to_remove.append(test_file_name)

            # Return the constructed folder for teardown function to remove
            return test_file_name, no_permission_folder
        
        def tearDown(no_permission_folder):

            # Firstly resume the permision of the folder to be removed
            os.chmod(no_permission_folder, 0o777)
            # Remove the folder
            shutil.rmtree(no_permission_folder)

        for file_extension, content in self.file_data.items():  
            super().setUp()
            test_file_name,no_permission_folder = setUp(file_extension,content)
            # print(test_file_name)
            try:
                # To test if the function fails to delete the file due to insufficient permission, returns false
                delete_success = delete_file(test_file_name)
                self.assertFalse(delete_success)

            finally:
                tearDown(no_permission_folder)
                super().tearDown()

        
# Class to identify and run test methods within TestFileOperations
class Test_runners(TestFileOperations):

    # For extract the test types
    def extract_test_type(self, test_name):
        try:
            # Split by "_", get the second part
            return test_name.split("_")[1]
        
        except IndexError:
            return "" 

    # Introspection for finding the corresponding tests inside test cases
    def find_test(self, prefix):
        test = []
        for name, func in TestFileOperations.__dict__.items():
            if callable(func) and name.startswith(prefix):
                test.append(getattr(self, name))
        return test
    
    # Run selected tests
    def run_tests(self, pattern=None):
        all_tests = self.find_test("test_")
        
        if pattern:
            # Filtering tests based on the pattern
            all_tests = [test for test in all_tests if pattern in self.extract_test_type(test.__name__)]
        
        # Define the report formats
        results = {"pass": 0, "fail": 0, "error": 0}
        test_num = 1 

        print("\n", "-"*50)  
        for test in all_tests:
            print(f"🔨Test #{test_num}: {test.__name__}")
            
            start_time = time.time()  
            try:
                test()
                results["pass"] += 1
                duration = time.time() - start_time 
                print(f"Status: ✅PASSED\nTime taken: {duration:.6f} seconds\n") 
            except AssertionError as ae:
                results["fail"] += 1
                print(f"Status: ❌FAILED\nReason: {ae}\n")
            except Exception as e:
                results["error"] += 1
                print(f"Status: ERROR\nReason: {e}\n")
            print("-"*50) 
            test_num += 1
        
        print(f"Total Results:\nPass: {results['pass']}\nFail: {results['fail']}\nError: {results['error']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific tests.")
    parser.add_argument('--select', type=str, help='Select tests to run based on a pattern in their name.')
    args = parser.parse_args()
    test_instance = Test_runners()
    test_instance.run_tests(pattern=args.select)