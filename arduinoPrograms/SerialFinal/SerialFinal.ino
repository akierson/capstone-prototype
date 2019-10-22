char inc;

void writeLetter(int pin1, int pin2) {
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, HIGH);

  delay(30);

  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
}

void writeLetterCap(int pin1, pin2) {
  digitalWrite(23, HIGH);
  digitalWrite(27, HIGH);
  writeLetter(pin1, pin2);
  digitalWrite(23, LOW);
  digitalWrite(27, LOW);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 22; i < 38; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
}

void loop() {
  if (Serial.available()) {
    inc = Serial.read();
    switch (inc) {
      case 'n':
        writeLetter(22, 31);
        break;
      case 'h':
        writeLetter(22, 32);
        break;
      case 'y':
        writeLetter(22, 33);
        break;
      case 'j':
        writeLetter(22, 36);
        break;
      case 'b':
        writeLetter(24, 31);
        break;
      case 'g':
        writeLetter(24, 32);
        break;
      case 't':
        writeLetter(24, 33);
        break;
      case '\n':
        writeLetter(24, 36);
        break;
      case 'v':
        writeLetter(25, 31);
        break;
      case 'f':
        writeLetter(25, 32);
        break;
      case 'r':
        writeLetter(25, 33);
        break;
      case 'm':
        writeLetter(25, 37);
        break;
      case 'c':
        writeLetter(26, 31);
        break;
      case 'd':
        writeLetter(26, 32);
        break;
      case 'e':
        writeLetter(26, 33);
        break;
      case 'p':
        writeLetter(26, 36);
        break;
      case 'x':
        writeLetter(27, 31);
        break;
      case 's':
        writeLetter(27, 32);
        break;
      case 'w':
        writeLetter(27, 33);
        break;
      case 'o':
        writeLetter(27, 36);
        break;
      case 'z':
        writeLetter(28, 31);
        break;
      case 'a':
        writeLetter(28, 32);
        break;
      case 'q':
        writeLetter(28, 33);
        break;
      case 'i':
        writeLetter(28, 36);
        break;
      case 'l':
        writeLetter(28, 37);
        break;
      case 'u':
        writeLetter(29, 36);
        break;
      case 'k':
        writeLetter(29, 37);
        break;
      case ' ':
        writeLetter(23, 25);
        break;
      case 'N':
        writeLetterCap(22, 31);
        break;
      case 'H':
        writeLetterCap(22, 32);
        break;
      case 'Y':
        writeLetterCap(22, 33);
        break;
      case 'J':
        writeLetterCap(22, 36);
        break;
      case 'B':
        writeLetterCap(24, 31);
        break;
      case 'G':
        writeLetterCap(24, 32);
        break;
      case 'T':
        writeLetterCap(24, 33);
        break;
      case 'V':
        writeLetterCap(25, 31);
        break;
      case 'F':
        writeLetterCap(25, 32);
        break;
      case 'R':
        writeLetterCap(25, 33);
        break;
      case 'M':
        writeLetterCap(25, 37);
        break;
      case 'C':
        writeLetterCap(26, 31);
        break;
      case 'D':
        writeLetterCap(26, 32);
        break;
      case 'E':
        writeLetterCap(26, 33);
        break;
      case 'P':
        writeLetterCap(26, 36);
        break;
      case 'X':
        writeLetterCap(27, 31);
        break;
      case 'S':
        writeLetterCap(27, 32);
        break;
      case 'W':
        writeLetterCap(27, 33);
        break;
      case 'O':
        writeLetterCap(27, 36);
        break;
      case 'Z':
        writeLetterCap(28, 31);
        break;
      case 'A':
        writeLetterCap(28, 32);
        break;
      case 'Q':
        writeLetterCap(28, 33);
        break;
      case 'I':
        writeLetterCap(28, 36);
        break;
      case 'L':
        writeLetterCap(28, 37);
        break;
      case 'U':
        writeLetterCap(29, 36);
        break;
      case 'K':
        writeLetterCap(29, 37);
        break;
      default:
        break;
    }
  }
}
