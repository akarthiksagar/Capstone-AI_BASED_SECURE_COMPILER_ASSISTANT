def main(): {
    # Variable declaration
    count = 10
    name = "User"
    
    # Function call
    print(name)
    
    # Control flow
    if count > 5: {
        print("Count is greater than 5")
    }
    
    # Semantic Check: call undefined function
    # undefined_func() 
    
    # Security Check: Dangerous functions
    cmd = "echo hello"
    # os.system(cmd)
    
    # Another dangerous one
    eval("print('hacked')")
}

main()
