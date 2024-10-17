from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from tabulate import tabulate
import subprocess

class StreamCapture:
    def __init__(self):
        self.output = ""

    def write(self, text):
        self.output += text

    def flush(self):
        pass  # This might be necessary depending on Python version

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(887, 1000)
        
        available_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        window_geometry = MainWindow.frameGeometry()
        window_geometry.moveCenter(available_geometry.center())
        MainWindow.move(window_geometry.topLeft())
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 10, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(48)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 171, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.GrammarInput = QtWidgets.QTextEdit(self.centralwidget)
        self.GrammarInput.setGeometry(QtCore.QRect(30, 100, 256, 192))
        self.GrammarInput.setObjectName("GrammarInput")
        self.outputWin = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputWin.setGeometry(QtCore.QRect(10, 300, 871, 521))
        self.outputWin.setObjectName("outputWin")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(650, 80, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.StringInput = QtWidgets.QTextEdit(self.centralwidget)
        self.StringInput.setGeometry(QtCore.QRect(610, 110, 256, 41))
        self.StringInput.setObjectName("StringInput")
        self.augGrammarBtn = QtWidgets.QPushButton(self.centralwidget)
        self.augGrammarBtn.setGeometry(QtCore.QRect(350, 100, 171, 32))
        self.augGrammarBtn.setObjectName("augGrammarBtn")
        self.dfaBtn = QtWidgets.QPushButton(self.centralwidget)
        self.dfaBtn.setGeometry(QtCore.QRect(350, 140, 171, 32))
        self.dfaBtn.setObjectName("dfaBtn")
        self.parseTableBtn = QtWidgets.QPushButton(self.centralwidget)
        self.parseTableBtn.setGeometry(QtCore.QRect(350, 180, 171, 32))
        self.parseTableBtn.setObjectName("parseTableBtn")
        self.parseStringBtn = QtWidgets.QPushButton(self.centralwidget)
        self.parseStringBtn.setGeometry(QtCore.QRect(350, 220, 171, 32))
        self.parseStringBtn.setObjectName("parseStringBtn")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 0, 100, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.augGrammarBtn.clicked.connect(self.on_augGrammarBtn_clicked)
        self.dfaBtn.clicked.connect(self.on_dfaBtn_clicked)
        self.parseTableBtn.clicked.connect(self.on_parseTableBtn_clicked)
        self.parseStringBtn.clicked.connect(self.on_parseStringBtn_clicked)
        self.pushButton_4.clicked.connect(self.open_other_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SLR Parser"))
        self.label.setText(_translate("MainWindow", "SLR"))
        self.label_2.setText(_translate("MainWindow", "Enter Valid Grammar"))
        self.label_3.setText(_translate("MainWindow", "Enter String to Parse"))
        self.augGrammarBtn.setText(_translate("MainWindow", "Augment Grammar"))
        self.dfaBtn.setText(_translate("MainWindow", "Construct DFA"))
        self.parseTableBtn.setText(_translate("MainWindow", "Construct Parsing Table"))
        self.parseStringBtn.setText(_translate("MainWindow", "Parse String"))
        self.pushButton_4.setText(_translate("MainWindow", "Back"))
        
    def open_other_file(self):
            # Close the current window
            MainWindow.close()

            # Start executing the other file
            FILE_PATH = "./main.py"
            try:
                subprocess.Popen([sys.executable, FILE_PATH])
            except Exception as e:
                print("Error executing file:", e)
        
        
    def compute_first_follow_sets(self,grammar, start_symbol):
        first = {non_terminal: set() for non_terminal in grammar.keys()}
        follow = {non_terminal: set() for non_terminal in grammar.keys()}
        follow[start_symbol].add('$')  # Assuming $ as EOF symbol

        # Function to find FIRST set for a specific sequence
        def first_of_sequence(sequence):
            result = set()
            for symbol in sequence:
                if not symbol.isupper():
                    result = {symbol}
                    break
                else:
                    result.update(first[symbol] - {'&'})
                    if '&' not in first[symbol]:
                        break
            return result

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.items():
                for production in productions:
                    # Find FIRST of each production
                    current_first = first_of_sequence(production)
                    # If new terminals are added, update the FIRST set
                    if not current_first.issubset(first[non_terminal]):
                        first[non_terminal].update(current_first)
                        changed = True

                    # Update FOLLOW sets
                    trail = set()
                    for i in range(len(production)-1, -1, -1):
                        symbol = production[i]
                        if symbol.isupper():
                            if not trail.issubset(follow[symbol]):
                                follow[symbol].update(trail)
                                changed = True
                            if '&' in first[symbol]:
                                trail.update(first[production[i+1:]] - {'&'})
                            else:
                                trail = first_of_sequence(production[i+1:])
                        else:
                            trail = {symbol}
                    if production and production[-1].isupper():
                        if not follow[non_terminal].issubset(follow[production[-1]]):
                            follow[production[-1]].update(follow[non_terminal])
                            changed = True

        return first, follow

    def parse_grammar(self, input_grammar):
        grammar = {}
        lines = input_grammar.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            parts = line.split('->')
            if len(parts) != 2:
                return None
            lhs, rhs = parts
            non_terminal = lhs.strip()
            productions = [prod.strip().split() for prod in rhs.split('|')]
            grammar[non_terminal] = productions
        return grammar
    

    def is_valid_grammar(self,grammar):
        defined_non_terminals = set(grammar.keys())
        used_non_terminals = set()
        for productions in grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol.isupper():  # Assuming non-terminals are uppercase
                        used_non_terminals.add(symbol)
        if not used_non_terminals.issubset(defined_non_terminals):
            return False
        if any(len(productions) == 0 for productions in grammar.values()):
            return False
        return True
        
    def generate_combinations(self, production, nullable):
        """Generate all combinations of a production by optionally removing nullable symbols."""
        results = [production]
        for i in range(len(production)):
            if production[i] in nullable:
                # For each nullable symbol, generate new combinations without it
                for comb in self.generate_combinations(production[:i] + production[i+1:], nullable):
                    if comb not in results:
                        results.append(comb)
        return results
    
    def remove_epsilon_productions(self,grammar):
        nullable = set()
        # Identify nullable non-terminals
        for non_terminal, productions in grammar.items():
            for production in productions:
                if '&' in production and len(production) == 1:
                    nullable.add(non_terminal)
        
        # Eliminate ε-productions and generate new ones
        new_grammar = {}
        for non_terminal, productions in grammar.items():
            new_productions = []
            for production in productions:
                if '&' in production and len(production) == 1:
                    continue  # Skip ε-productions directly
                # Include all combinations that result from nullable removals
                combinations = self.generate_combinations(production, nullable)
                for comb in combinations:
                    if comb not in new_productions:
                        new_productions.append(comb)
            new_grammar[non_terminal] = new_productions
        
        return new_grammar
    
    def determine_augmentation(self,grammar):
        # Determine the original start symbol
        original_start_symbol = next(iter(grammar))  # Assuming the first non-terminal is the start symbol

        # Create a new start symbol to ensure clarity and consistency in augmentation
        new_start_symbol = "S'"
        while new_start_symbol in grammar:  # Ensure the new symbol does not already exist in the grammar
            new_start_symbol += "'"

        # Create the new augmented grammar with the new start symbol and end-of-input marker
        augmented_grammar = {new_start_symbol: [[original_start_symbol, '$']]}
        augmented_grammar.update(grammar)
        return augmented_grammar, new_start_symbol, '$'
    
    
    def closure(self,items, grammar, labeled_grammar):
        closure_set = set(items)
        added = True
        while added:
            new_items = set()
            for (non_terminal, production, pos, rule_index) in closure_set:
                if pos < len(production) and production[pos] in grammar:
                    next_symbol = production[pos]
                    for prod in grammar[next_symbol]:
                        for index, (lhs, prod_rhs) in labeled_grammar.items():
                            if lhs == next_symbol and tuple(prod_rhs) == tuple(prod):
                                item = (next_symbol, tuple(prod), 0, index)
                                if item not in closure_set:
                                    new_items.add(item)
            if new_items:
                closure_set.update(new_items)
            else:
                added = False
        return closure_set
    

    def label_productions(self, grammar):
        labeled_grammar = {}
        label_index = 0
        for non_terminal, productions in grammar.items():
            for production in productions:
                labeled_grammar[label_index] = (non_terminal, production)
                label_index += 1
        return labeled_grammar
    

    def goto(self,items, symbol, grammar, labeled_grammar):
        goto_set = set()
        for item in items:
            non_terminal, production, pos, rule_index = item
            if pos < len(production) and production[pos] == symbol:
                moved_item = (non_terminal, production, pos + 1, rule_index)
                goto_set.add(moved_item)
        return self.closure(goto_set, grammar, labeled_grammar)
    
    
    
    def items(self,grammar, start_symbol, labeled_grammar, eof_symbol):
        # Fetch the rule index for the starting rule
        start_index = next(index for index, (lhs, rhs) in labeled_grammar.items() if lhs == start_symbol and rhs == grammar[start_symbol][0])
        initial_item = (start_symbol, tuple(grammar[start_symbol][0]), 0, start_index)
        initial_closure = self.closure({initial_item}, grammar, labeled_grammar)
        states = [sorted(initial_closure, key=lambda x: x[3])]
        transitions = {}
        accept_states = set()
        all_symbols = set(sym for prods in grammar.values() for prod in prods for sym in prod if sym != eof_symbol)

        added = True
        while added:
            added = False
            new_states = []
            for state in states:
                for symbol in all_symbols:
                    g = self.goto(state, symbol, grammar, labeled_grammar)
                    if g:
                        g_sorted = sorted(g, key=lambda x: x[3])
                        if g_sorted not in states:
                            new_states.append(g_sorted)
                            transitions[(states.index(state), symbol)] = len(states) + new_states.index(g_sorted)
                        elif g_sorted:
                            transitions[(states.index(state), symbol)] = states.index(g_sorted)
            if new_states:
                states.extend(new_states)
                added = True
        for i, state in enumerate(states):
            for item in state:
                non_terminal, production, pos, rule_index = item
                if pos == len(production) - 1 and non_terminal == start_symbol and production[-1] == eof_symbol:
                    accept_states.add(i)
        return states, transitions, all_symbols, accept_states
        
    


    def construct_parsing_table(self,states, transitions, grammar, labeled_grammar, start_symbol, accept_states, follow_sets):
        terminals = {sym for prods in grammar.values() for prod in prods for sym in prod if not any(sym in non_terminal for non_terminal in grammar)}
        non_terminals = set(grammar.keys())

        action_table = {}
        goto_table = {}
        conflicts = []

        for (from_state, symbol), to_state in transitions.items():
            if symbol in terminals:
                action = ('shift', to_state)
                if (from_state, symbol) in action_table:
                    existing_action = action_table[(from_state, symbol)]
                    if existing_action[0] == 'reduce':
                        conflicts.append(("Shift-Reduce", from_state, symbol, existing_action, action))
                action_table[(from_state, symbol)] = action
            elif symbol in non_terminals:
                goto_table[(from_state, symbol)] = to_state

        accept_state = accept_states.pop()  # Assuming only one accept state for simplicity
        action_table[(accept_state, '$')] = ('accept',)

        for i, state in enumerate(states):
            for item in state:
                head, body, pos, rule_index = item
                if pos == len(body):
                    follow_symbols = follow_sets[head]
                    for terminal in follow_symbols:
                        action = ('reduce', rule_index)
                        if (i, terminal) in action_table:
                            existing_action = action_table[(i, terminal)]
                            if existing_action[0] == 'shift':
                                conflicts.append(("Shift-Reduce", i, terminal, existing_action, action))
                            elif existing_action[0] == 'reduce' and existing_action[1] != rule_index:
                                conflicts.append(("Reduce-Reduce", i, terminal, existing_action, action))
                        else:
                            action_table[(i, terminal)] = action

        return action_table, goto_table, conflicts

    
    
    
    def parse_string(self,input_string, action_table, goto_table, start_symbol, labeled_grammar):
        old_stdout = sys.stdout
        captured_output = StreamCapture()
        sys.stdout = captured_output
        try:
            tokens = input_string.split() + ['$'] 
            stack = [0]  
            index = 0

            while index < len(tokens):
                current_token = tokens[index]
                state = stack[-1]
                action_entry = action_table.get((state, current_token))
                print(f"Current State: {state}, Current Token: {current_token}, Action Entry: {action_entry}, Stack: {stack}")
                if action_entry is None:
                    print("Error: Unexpected token or no rule applicable")
                    print("Failure: The input string is not accepted by the grammar")
                    return "Error: Unexpected token or no rule applicable."
                action = action_entry[0] 
                if action == 'shift':
                    value = action_entry[1]
                    stack.append(value)
                    index += 1
                elif action == 'reduce':
                    value = action_entry[1]
                    _, production = labeled_grammar[value]
                    for _ in range(len(production)):
                        stack.pop()
                    top_state = stack[-1]
                    non_terminal = labeled_grammar[value][0]
                    goto_state = goto_table.get((top_state, non_terminal))
                    stack.append(goto_state)
                elif action == 'accept':
                    print("Success: The input string is accepted by the grammar")
                    return "Success: The input string is accepted by the grammar."
            print("Error: Reached end of input without acceptance.")
            print("Failure: The input string is not accepted by the grammar")
            return "Error: Reached end of input without acceptance."

        finally:
            sys.stdout = old_stdout
            return captured_output.output

    
    
    def on_augGrammarBtn_clicked(self):
        input_grammar = self.GrammarInput.toPlainText()
        print("Input Grammar:", input_grammar)  
        if not input_grammar.strip():
            self.outputWin.setPlainText("No grammar provided. Please enter a valid grammar.")
            return
        output = self.augmentGrammar(input_grammar)
        print(f"Output to display: {output}")
        self.outputWin.setPlainText(output if output else "No output generated by augmentGrammar.")

    def augmentGrammar(self, input_grammar):
        old_stdout = sys.stdout
        captured_output = StreamCapture()
        sys.stdout = captured_output
        try:
            grammar = self.parse_grammar(input_grammar)
            if grammar is None or not self.is_valid_grammar(grammar):
                print("Invalid or improperly formatted grammar provided.")
            else:
                # Assuming we augment the grammar here
                print("Grammar parsed and validated successfully.")
                
                
                new_grammar = self.remove_epsilon_productions(grammar)
                for non_terminal, productions in new_grammar.items():
                    print(f"{non_terminal} -> {' | '.join([' '.join(prod) for prod in productions])}")
             
                print("Augmented Grammar:")
                augmented_grammar, start_symbol, eof_symbol = self.determine_augmentation(new_grammar)
                labeled_grammar = self.label_productions(augmented_grammar) 
                
                for label, rule in labeled_grammar.items():
                    production = ' '.join(rule[1])
                    print(f"({label}) {rule[0]} -> {production}") 
                    print() 
                first_sets, follow_sets = self.compute_first_follow_sets(augmented_grammar, start_symbol)
                print("First Sets:")
                for non_terminal in first_sets:
                    print(f"First({non_terminal}) = {first_sets[non_terminal]}")
                print() 
                print("Follow Sets:")
                for non_terminal in follow_sets:
                    print(f"First({non_terminal}) = {follow_sets[non_terminal]}")           
                
                
        finally:
            sys.stdout = old_stdout
        return captured_output.output

        
    
    def on_dfaBtn_clicked(self):
        print("Augment DFA Button clicked")  # Correct button description
        input_grammar = self.GrammarInput.toPlainText()
        if not input_grammar.strip():
            self.outputWin.setPlainText("No grammar provided. Please enter a valid grammar.")
            return
        output = self.dfa(input_grammar)
        print(f"Output to display: {output}")
        self.outputWin.setPlainText(output if output else "No output generated by DFA function.")

    def dfa(self, input_grammar):
        old_stdout = sys.stdout
        captured_output = StreamCapture()
        sys.stdout = captured_output
        try:
            grammar = self.parse_grammar(input_grammar)
            if grammar is None or not self.is_valid_grammar(grammar):
                print("Invalid or improperly formatted grammar provided.")
            else:
                print("Grammar parsed and validated successfully.")
                new_grammar = self.remove_epsilon_productions(grammar)
                augmented_grammar, start_symbol, eof_symbol = self.determine_augmentation(new_grammar)
                labeled_grammar = self.label_productions(augmented_grammar)
                first_sets, follow_sets = self.compute_first_follow_sets(augmented_grammar, start_symbol)
                states, transitions, all_symbols, accept_states = self.items(augmented_grammar, start_symbol, labeled_grammar, eof_symbol)
                print("DFA States and Transitions:")
                for i, state in enumerate(states):
                    print(f"I{i}:")
                    for item in state:
                        non_terminal, production, pos, rule_index = item
                        production_display = ' '.join(production[:pos] + ('.',) + production[pos:])
                        print(f"{non_terminal} -> {production_display}")
                    print("------------------")
                print("Transitions:")
                for (from_state, symbol), to_state in transitions.items():
                    print(f"transition(I{from_state}, {symbol}) -> I{to_state}")
                print("Accept States:")
                for accept_state in accept_states:
                    print(f"I{accept_state} is an accept state.")
        finally:
            sys.stdout = old_stdout
        return captured_output.output
    
    
    def on_parseTableBtn_clicked(self):
        print("Constructing parse table...")
        input_grammar = self.GrammarInput.toPlainText()
        if not input_grammar.strip():
            self.outputWin.setPlainText("No grammar provided. Please enter a valid grammar.")
            return
        output = self.parseTable(input_grammar)
        self.outputWin.setPlainText(output if output else "Failed to generate parsing table.")


    


    def parseTable(self, input_grammar):
        old_stdout = sys.stdout
        captured_output = StreamCapture()
        sys.stdout = captured_output
        try:
            grammar = self.parse_grammar(input_grammar)
            if grammar is None or not self.is_valid_grammar(grammar):
                print("Invalid grammar. Please check the input format and retry.")
            else:
                new_grammar = self.remove_epsilon_productions(grammar)
                augmented_grammar, start_symbol, eof_symbol = self.determine_augmentation(new_grammar)
                labeled_grammar = self.label_productions(augmented_grammar)
                first_sets, follow_sets = self.compute_first_follow_sets(augmented_grammar, start_symbol)
                states, transitions, all_symbols, accept_states = self.items(augmented_grammar, start_symbol, labeled_grammar, eof_symbol)
                action_table, goto_table, conflicts = self.construct_parsing_table(states, transitions, augmented_grammar, labeled_grammar, start_symbol, accept_states,follow_sets)

                all_symbols = sorted(set(action_table.keys()) | set(goto_table.keys()), key=lambda x: (x[1], x[0]))
                symbols = sorted(set(sym for state, sym in all_symbols))
                
                if conflicts:
                    print("The Grammar is not SLR:")
                    print("Conflicts Detected:")
                    for conflict in conflicts:
                        print(f"State {conflict[0]}, Symbol '{conflict[1]}', Conflict Type: {conflict[2]}, Actions: {conflict[3]} vs {conflict[4]}")
                else:
                    print("The Grammar is SLR:")
                
                print("\nAction Table:")
                for key, value in sorted(action_table.items()):
                    print(f"State {key[0]}, on symbol '{key[1]}' -> {value}")

                print("\nGoto Table:")
                for key, value in sorted(goto_table.items()):
                    print(f"State {key[0]}, on symbol '{key[1]}' -> State {value}")
                print()            
                # Fixed width based on the longest word "State/Action"
                width = len("State/Action") + 2  # Adding some padding

                head = f"{'State/Action'.ljust(width)}"
                for symbol in symbols:
                    head += f"{symbol.ljust(width)}"
                print(head)
                print("-" * len(head))

                states = sorted(set(state for state, symbol in all_symbols))
                for state in states:
                    line = f"{f'State {state}'.ljust(width)}"
                    for symbol in symbols:
                        action = action_table.get((state, symbol), "")
                        if isinstance(action, int):
                            if action > 0:
                                action = f"s{action}"
                            elif action < 0:
                                action = f"r{abs(action)}"
                        line += f"{str(action).ljust(width)}"
                    print(line)
                    print("-" * len(head))
                
        finally:
            sys.stdout = old_stdout
        return captured_output.output




    
    
    def on_parseStringBtn_clicked(self):
        print("Augment parse string Button clicked")
        input_grammar = self.GrammarInput.toPlainText()
        input_string = self.StringInput.toPlainText()
        output = self.StringParse(input_grammar, input_string)
        self.outputWin.setPlainText(output)
        


    def StringParse(self, input_grammar, input_string):
        old_stdout = sys.stdout
        captured_output = StreamCapture()
        sys.stdout = captured_output
        try:
            grammar = self.parse_grammar(input_grammar)
            if grammar is None or not self.is_valid_grammar(grammar):
                print("Invalid grammar.")
            else:
                new_grammar = self.remove_epsilon_productions(grammar)
                augmented_grammar, start_symbol, eof_symbol = self.determine_augmentation(new_grammar)
                labeled_grammar = self.label_productions(augmented_grammar)
                first_sets, follow_sets = self.compute_first_follow_sets(augmented_grammar, start_symbol)
                states, transitions, all_symbols, accept_states = self.items(augmented_grammar, start_symbol, labeled_grammar, eof_symbol)
                action_table, goto_table, conflicts = self.construct_parsing_table(states, transitions, augmented_grammar, labeled_grammar, start_symbol, accept_states,follow_sets)
                result = self.parse_string(input_string, action_table, goto_table, start_symbol, labeled_grammar)
                print(result)              
                
        finally:
            sys.stdout = old_stdout
        
        # Prepare the output to be displayed
        if result:
            display_output = result
        else:
            display_output = "No output generated by parse_string."
        
        return display_output


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
