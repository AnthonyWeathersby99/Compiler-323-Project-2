from grammar import grammar, parsing_table

def parse_input(input_string):
    # Split input into tokens and append the end symbol '$'
    tokens = input_string.split() + ['$']

    # Initialize stack
    stack = [0]

    # Pointer to track the current position in the token list
    pointer = 0

    # Step counter to track the number of actions taken
    step = 0

    # Token Processing
    while pointer < len(tokens):
        # Get current token to process
        current_input = tokens[pointer]

        # Retrieve current state from top of the stack
        state = stack[-1]

        # Fetch the action from the parsing table based on the current state and token
        action = parsing_table.get((state, current_input))

        # Increment the step counter and print state
        step += 1
        print(f"Step: {step}, Stack: {stack}, Input: {tokens[pointer:]}, Action: {action}")

        # If no action, string is not accepted
        if action is None:
            return "String is not accepted"

        # If the action is a shift ('S'), push the token and its resulting state onto the stack
        if action.startswith('S'):
            stack.append(current_input)
            stack.append(int(action[1:]))
            pointer += 1

        # If the action is a reduce ('R'), execute the reduction based on the grammar rule
        elif action.startswith('R'):
            # Retrieve the rule associated
            rule_key = action
            production = grammar[rule_key]

            # Pop elements from the stack corresponding to the symbols
            for _ in range(2 * len(production[0])):  # Each symbol has a corresponding state
                stack.pop()

            # Get the non-terminal from the production rule to push back to the stack
            non_terminal = production[1]

            # Check the stack for the current state after reduction
            top_state = stack[-1]

            # Fetch the next state from the GOTO part of the parsing table
            next_state = parsing_table.get((top_state, non_terminal))

            # If there is no valid GOTO entry, return an error
            if next_state is None:
                return f"No GOTO entry for (state: {top_state}, non-terminal: {non_terminal})"

            # Push the non-terminal and its state onto the stack
            stack.append(non_terminal)
            stack.append(next_state)

        # Action is 'acc', string = successfully parsed
        elif action == 'acc':
            return "String is accepted"

    return "String is not accepted"

# Test the parser
input_string1 = "( id + id ) * id $"
result1 = parse_input(input_string1)
print("String: " + input_string1 + ": ", result1 + '\n')

input_string2 = "id * id $"
result2 = parse_input(input_string2)
print("String: " + input_string2 + ": ", result2 + '\n')

input_string3 = "( id * ) $"
result3 = parse_input(input_string3)
print("String: " + input_string3 + ": ", result3)
