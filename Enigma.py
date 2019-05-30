import string

alp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class Enigma:

    def __init__(self, rotor1, rotor2, rotor3, reflector, start_position = 'AAA', steckers='', mute = False ):

        self.rotors = [rotor3, rotor2, rotor1]
        self.reflector = list(reflector)
        self.substitutions = [] #[('a', 'u'), ('b', 'g'), ('c', 'n'), ('d', 'p'), ('e', 'c'), ('f', 'd'), ('g', 'a'), ('h', 'w'), ('i', 'k')]

        i = 0
        self.start_position = start_position
        for r in reversed(self.rotors):
            r.set_start_position(start_position[i])
            r.mute = mute 
            i += 1

        self.steckers = steckers
        self.stecker_name = self.steckers
        steckers = steckers.replace(' ','')
        steckers_temp = []
        i = 0 
        while i < len(steckers):
            steckers_temp.append((steckers[i], steckers[i + 1]))
            steckers_temp.append(((steckers[i + 1], steckers[i])))
            i += 2
        self.steckers = steckers_temp
        if self.rotors[0].has_to_switch() :
            self.rotors[1].turn()
            if self.rotors[1].has_to_switch():
                self.rotors[2].turn()


    def get_subst_permuted(self, letter):
        for s in self.substitutions:
            if letter == s[0]:
                letter = s[1]
                break
    
    def get_rotors_permuted(self, letter):
        letter = (string.ascii_lowercase.index(letter[1].lower()), letter)
        for r in self.rotors:
            letter = r.get_permuted(letter)
        return letter

    def get_rotors_back_permuted(self, letter):
        for r in reversed(self.rotors):
            letter = r.get_permuted_back(letter)
        pos_temp = self.rotors[0].alp_out.index(letter[1])
        return (pos_temp, alp[pos_temp])

    def get_reflector_permuted(self, letter) : 
        letter_o = self.reflector[letter[0]]
        return (alp.index(letter_o), letter_o)

    def display_reflector(self):
        a = ''
        b = '' 
        i = 0
        for x in reflector:
            a += alp[i] + ' '
            b += x + ' '
            i += 1
        print('REFLECTOR ')
        print(a)
        print(b)
        print()
            

    def turn_rotors(self):
        self.rotors[0].turn()
        if self.rotors[0].has_to_switch() :
            self.rotors[1].turn()
            if self.rotors[1].has_to_switch():
                self.rotors[2].turn()

    def turn_rotors_backward(self):
        self.rotors[0].turn_backward()
        if self.rotors[0].has_to_switch_backward() :
            self.rotors[1].turn_backward()
            if self.rotors[1].has_to_switch_backward():
                self.rotors[2].turn_backward()

    def display_rotors(self):
        i = 1 
        for r in self.rotors:
            print('POS ' + str(i))
            r.display()
            i += 1

    def get_steckers_permuted(self, letter):
        letter_temp = letter[1]
        for perm in self.steckers:
            if letter_temp == perm[0]:
                letter_temp = perm[1]
                break
        
        return (alp.index(letter_temp), letter_temp)
    
    def display_steckers(self):
        a = ''
        b = ''
        for i in self.steckers:
            a += i[0] + ' '
            b += i[1] + ' '
        print('STECKERS : ')
        print(a)
        print(b)
        print()

    def display_settings(self):
        print()
        print('SETTINGS : {}'.format(self.rotors[2].name + ' ' + self.rotors[1].name + ' ' + self.rotors[0].name + ' ' + self.start_position + ' ' + self.stecker_name))
        print('ROTORS : ' + self.rotors[2].name + ' ' + self.rotors[1].name + ' ' + self.rotors[0].name)
        print('ROTORS START POSITION : ' + self.start_position)
        print('STECKERS : ' + self.stecker_name)
        print()

    def display_rotors_settings(self):
        print()
        print('ROTORS POSITION : {}'.format(self.rotors[2].alp_out[0] + ' ' + self.rotors[1].alp_out[0] + ' ' + self.rotors[0].alp_out[0]))
        print()

    def get_rotors_settings(self, minus = 0):
        if minus > 0 :
            for x in range(0, minus):
                self.turn_rotors_backward()
        return '{}'.format(self.rotors[2].alp_out[0] + ' ' + self.rotors[1].alp_out[0] + ' ' + self.rotors[0].alp_out[0])

            

    
    def get_letter_permuted(self, letter):
        letter = self.get_steckers_permuted(letter)
        letter = self.get_rotors_permuted(letter)
        letter = self.get_reflector_permuted(letter)
        letter = self.get_rotors_back_permuted(letter)
        letter = self.get_steckers_permuted(letter)
        return letter 




class Rotor:

    def __init__(self, name, permutations, switch, start_position = 'A'):
        self.CONST_PERM = list(permutations)
        self.permutations = list(permutations)
        self.name = name
        self.alp_out = alp
        self.switch = switch
        self.position = ''
        self.mute = False 

    def turn(self):
        perm_temp = self.permutations[0]
        self.permutations = self.permutations[1:]
        self.permutations.append(perm_temp)

        alp_out_temp = self.alp_out[0]
        self.alp_out = self.alp_out[1:]
        self.alp_out.append(alp_out_temp)   

        if self.mute != True: 
            print('ROTOR ' + self.name + ' TOURNE \n')     
    
    def turn_backward(self):
        self.permuation = [self.permutations[-1]] + self.permutations
        self.permuation.pop()

        self.alp_out = [self.alp_out[-1]] + self.alp_out
        self.alp_out.pop()
        if self.mute != True: 
            print('ROTOR ' + self.name + ' TOURNE BACK \n ')
                    
    def display(self):
        alp_temp = ''
        for letter in self.alp_out:
            alp_temp += letter + ' '
        perm_temp = ''
        for l in self.permutations:
            perm_temp += l + ' '
        x = ''
        for i in range(0, 26):
            x += str(i) + ' '
        print('ROTOR : ' + self.name)
        #print('N : ' + str(x))
        print('A : ' + str(alp_temp))
        print('P : ' + str(perm_temp))
        print()

    def has_to_switch(self):
        if self.alp_out[-1] == self.switch and self.alp_out[0] == chr(ord(self.switch) + 1) :
            return True
        else:
            return False

    def has_to_switch_backward(self):
        if self.alp_out[0] == self.switch:
            return True
        else:
            return False

    
    def get_permuted(self, letter):
        letter_o = self.permutations[letter[0]]
        return (self.alp_out.index(letter_o), letter_o)

    def get_permuted_back(self, letter):
        letter_temp = self.alp_out[letter[0]]
        pos_letter_o = self.permutations.index(letter_temp)
        letter_o = self.alp_out[pos_letter_o]
        return(pos_letter_o, letter_o)

    def set_start_position(self, letter):
        pos_temp = alp.index(letter)
        i = 0 
        while i < pos_temp:
            alp_out_temp = self.alp_out[0]
            self.alp_out = self.alp_out[1:]
            self.alp_out.append(alp_out_temp)

            perm_temp = self.permutations[0]
            self.permutations = self.permutations[1:]
            self.permutations.append(perm_temp)

            i += 1


#ROTORS 
I = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
II = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
III = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
IV = Rotor('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
V = Rotor('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

#REFLECTORS : 
A = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

if __name__ == "__main__":

    #Enigma initialization 
    enigma = Enigma(I, II, III, A, start_position='AAA', steckers='')

    msg = 'hello world'
    enigma.display_settings()
    msg = str(input('Entrer texte à chiffrer/déchiffrer :\n'))
    msg = msg.upper()
    msg_ciphered = ''
    i = 1
    for letter in msg:
        if letter in alp:
            letter = (alp.index(letter), letter)
            enigma.turn_rotors()
            enigma.display_rotors_settings()
            print(letter)
            letter = enigma.get_steckers_permuted(letter)
            letter = enigma.get_rotors_permuted(letter)
            letter = enigma.get_reflector_permuted(letter)
            letter = enigma.get_rotors_back_permuted(letter)
            letter = enigma.get_steckers_permuted(letter)
            print(letter[1] + ' ' + str(i))
            msg_ciphered += letter[1]
            i += 1
        else:
            msg_ciphered += letter
    print(msg_ciphered)
