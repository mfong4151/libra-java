# libra-java

Smart copy pasting to your 


    ## TODO feed the following prompt to chatgpt and integrate
      """
      This is libra-java, a cli to copy paste java classes in an organized fashion. I want you to create a class based off the else 
      branch in the main.py file, which specifically copies all the functions in a file, and any imports it relies on.
      
      I want you to create a stylistically similar function that does the following.
      - Given the name of a java class and method belonging to the class (instance or method), copies the enitre java class method first. Rely on the libra-config.json cache file for this
      - As a setup process, identifies all the dependencies that are dependency injected. This can be identified by extracting the constructor into a variable
      - Finds the method name given in the cli
      - Finds the private methods used 
      - Then, copies all of the imported functions relying on the package keywords. We can decypher their location from the import statements at the top of the page. We should redo the 3 steps above again for each class method
      - If the functions cannot be found, ignore them. 
      - Copies all of the code to the keyboard 
      
      """