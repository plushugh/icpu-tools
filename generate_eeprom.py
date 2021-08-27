from os import getcwd
from pathlib import Path

from optparse import OptionParser

from control_words_to_hex import control_words_to_hex

parser = OptionParser(
    description='Generate eeprom file based on instructions and config')

parser.add_option('--digital', dest='digital',
                  help='generates digital compatible output (default=True)', default=True)
parser.add_option('-d', '--dir', dest='dir', type='string',
                  help='directory of instructions and config file')
parser.add_option('-s', '--size', dest='size', type='int',
                  help='size of the eeprom (in instructions) (default=32)', default=32)
parser.add_option('-e', '--ext', dest='ext', type='string',
                  help='file extension of instructions (with dot) (default=.inst)', default='.inst')
parser.add_option('-c', '--config', dest='config', type='string',
                  help='file name of config file in DIR (default=config)', default='config')
parser.add_option('-o', '--out', dest='out', type='string',
                  help='file name of output eeprom file in DIR (default=dump.hex)', default='dump.hex')

options, args = parser.parse_args()


def main():
    instructions_list_file_path = Path(getcwd(), options.dir, options.config)
    instructions: list[str] = []
    entries: dict[int, str] = {}

    if(options.dir is None):
        print('Please add directory of instructions and config')
        exit(1)

    print('Reading config file:')

    with open(instructions_list_file_path, 'r') as instructions_list_file:
        for entry in instructions_list_file.readlines():
            entry = entry.rstrip('\n')
            instruction_addr, instruction_name = entry.split(' ')
            entries[int(instruction_addr, base=0)] = instruction_name
            print(
                f'    Queue: queued adding instruction {instruction_name} at {hex(int(instruction_addr, base=0))}')
        pass

    print('Adding instructions:')

    for i_addr in range(options.size):
        if i_addr in entries:
            instruction_path = Path(
                getcwd(), options.dir, entries[i_addr] + options.ext)
            with open(instruction_path, 'r') as instruction_file:
                instruction_file_raw: list[str] = instruction_file.readlines()
                instruction: list[str] = []
                for line in instruction_file_raw:
                    line = line.rstrip('\n')
                    if line == '0':
                        instruction.append('0000')
                    else:
                        instruction_line = line.split(',')
                        try:
                            instruction_line_hex = control_words_to_hex(
                                set(instruction_line))
                            instruction.append(instruction_line_hex)
                        except ValueError:
                            raise ValueError(
                                f'Error at file {instruction_path}')
                        pass
                    pass
                if len(instruction_file_raw) < 16:
                    for _ in range(16 - len(instruction_file_raw)):
                        instruction.append('0000')
                    pass
                if len(instruction_file_raw) > 16:
                    raise ValueError(
                        f'Instruction {entries[i_addr]} is too long')
                instructions.extend(instruction)
                print(f'    Added instruction {entries[i_addr]}')
                pass
        else:
            for _ in range(16):
                instructions.append('0000')
            pass
            print(
                f'    Instruction at {hex(i_addr)} does not exist, added 16 o\'s')
        pass

    dump_path = Path(getcwd(), options.dir, options.out)
    print(f'Dumping instructions into {dump_path}')
    with open(dump_path, 'w+') as dump_file:
        if (options.digital):
            dump_file.write('v2.0 raw\n')
        for line in instructions:
            dump_file.write(line + '\n')
        pass
    pass


if __name__ == '__main__':
    main()
