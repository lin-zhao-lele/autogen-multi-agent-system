def say_hello(
        target: str = "World") -> None:
    print(f"Hello, {target}!")

""" Prints a customizable 'Hello!' message to the standard output. This function demonstrates a basic program structure by encapsulating the greeting logic within a function and using a main guard to make the script executable while also allowing it to be imported as a module. Args: target (str): The entity or name to greet. Defaults to "World" if no argument is provided, resulting in the classic "Hello, World!" message. """



if __name__ == "__main__":
    say_hello()

# This block ensures that 'say_hello()' is called only when the script
# is executed directly (e.g., `python your_script_name.py`),
# not when it's imported as a module into another script. say_hello()
