from parsing import *
from parsing.grammar import *
import sys
import samples


def get_grammar():
    return samples.get_sample_9()


def read_grammar(filename):
    non_terminals = []
    with open(filename, 'r') as f:
        nt = ""
        productions = []
        for i, l in enumerate(f, 1):
            comment_pos = l.find("//")
            if comment_pos != -1:
                l = l[:comment_pos]
            l = l.replace("/* empty */", "EMPTY")
            if l == "":
                pass
            elif l[0] == " ":
                production = l.strip().split(" ")
                if len(production) == 1 and production[0] == "EMPTY":
                    production = []
                productions.append(production)
            else:
                l = l.strip()
                colon_pos = l.find(":")
                if colon_pos != -1:
                    if nt != "":
                        non_terminals.append(NonTerminal(nt, productions))
                    nt = l[:colon_pos]
                    productions = []
        if nt != "":
            non_terminals.append(NonTerminal(nt, productions))
    grammar = Grammar(non_terminals)

    return grammar


def describe_grammar(gr):
    return '\n'.join([
        'Indexed grammar rules (%d in total):' % len(gr.productions),
        str(gr) + '\n',
        'Grammar non-terminals (%d in total):' % len(gr.nonterms),
        '\n'.join('\t' + str(s) for s in gr.nonterms) + '\n',
        'Grammar terminals (%d in total):' % len(gr.terminals),
        '\n'.join('\t' + str(s) for s in gr.terminals)
    ])


def describe_parsing_table(table):
    conflict_status = table.get_conflict_status()

    def conflict_status_str(state_id):
        has_sr_conflict = (conflict_status[state_id] == lalr_one.STATUS_SR_CONFLICT)
        status_str = ('shift-reduce' if has_sr_conflict else 'reduce-reduce')
        return 'State %d has a %s conflict' % (state_id, status_str)

    return ''.join([
        'PARSING TABLE SUMMARY\n',
        'Is the given grammar LALR(1)? %s\n' % ('Yes' if table.is_lalr_one() else 'No'),
        ''.join(conflict_status_str(sid) + '\n' for sid in range(table.n_states)
                if conflict_status[sid] != lalr_one.STATUS_OK) + '\n',
        table.stringify()
    ])


def main():
    gr = read_grammar(sys.argv[1])
    print('Working on it...')
    table = lalr_one.ParsingTable(gr)
    print("I'm done.")
    table.generate_code(sys.argv[2])

    output_filename = 'parsing-table'

    with open(output_filename + '.txt', 'w') as textfile:
        textfile.write(describe_grammar(gr))
        textfile.write('\n\n')
        textfile.write(describe_parsing_table(table))

    """
    table.save_to_csv(output_filename + '.csv')
    """

if __name__ == "__main__":
    main()
