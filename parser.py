from grammar import grammar, parsing_table

def parse_input(input_string):
    tokens = input_string.split() + ['$']  # Tokenize and ensure end symbol
    stack = [0]  # Start with the initial state
    pointer = 0
    step = 0  # Initialize step counter

    while pointer < len(tokens):
        current_input = tokens[pointer]
        state = stack[-1]
        action = parsing_table.get((state, current_input))

        step += 1
        print(f"Step: {step}, Stack: {stack}, Input: {tokens[pointer:]}, Action: {action}")

        if action is None:
            return "String is not accepted"

        if action.startswith('S'):  # Shift action
            stack.append(current_input)
            stack.append(int(action[1:]))
            pointer += 1
        elif action.startswith('R'):  # Reduce action
            rule_key = action
            production = grammar[action]
            for _ in range(2 * len(production[0])):
                stack.pop()
            non_terminal = production[1]
            top_state = stack[-1]
            next_state = parsing_table.get((top_state, non_terminal))
            if next_state is None:
                return f"No GOTO entry for (state: {top_state}, non-terminal: {non_terminal})"
            stack.append(non_terminal)
            stack.append(next_state)
        elif action == 'acc':
            return "String is accepted"


# Output the results in the terminal for all 3 test cases
input_string1 = "( id + id ) * id $"
result1 = parse_input(input_string1)
print("String: " + input_string1 + ": ",result1+ '\n')

input_string2 = "id * id $"
result2 =parse_input(input_string2)
print("String: " + input_string2 + ": ",result2 + '\n')

input_string3 = "( id * ) $"
result3 = parse_input(input_string3)
print("String: " + input_string3 + ": ",result3)
