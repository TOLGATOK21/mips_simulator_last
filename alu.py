class ALU:
    def __init__(self):
        pass
# dasfksd
    def add(self, operand1, operand2):
        # İki operatörü toplar
        return operand1 + operand2

    def subtract(self, operand1, operand2):
        # İki operatörü çıkarır
        return operand1 - operand2

    def multiply(self, operand1, operand2):
        # İki operatörü çarpar
        return operand1 * operand2

    def divide(self, operand1, operand2):
        # İki operatörü böler
        if operand2 != 0:
            return operand1 / operand2
        else:
            print("Hata: Sıfıra bölme hatası")
            return None

    def bitwise_and(self, operand1, operand2):
        # İki operatör arasında bit düzeyinde "ve" işlemi yapar
        return operand1 & operand2

    def bitwise_or(self, operand1, operand2):
        # İki operatör arasında bit düzeyinde "veya" işlemi yapar
        return operand1 | operand2

    def bitwise_xor(self, operand1, operand2):
        # İki operatör arasında bit düzeyinde "özel veya" işlemi yapar
        return operand1 ^ operand2

    def bitwise_not(self, operand):
        # Operatörün bitlerini tersine çevirir (bitwise not işlemi)
        return ~operand
