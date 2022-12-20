from datetime import datetime
from tkinter import END, Menu, Text, Tk,N,E,W,S,BOTTOM,TOP,LEFT,RIGHT,X,Y,BOTH, filedialog, simpledialog;
from tkinter.ttk import *;
from PyQt5.QtWidgets import QApplication;
from PIL import Image, ImageTk,ImageOps
import pyperclip;
import Style as SetStyle,os,sys,ctypes as ct,threading as thread,darkdetect as d,idlelib.colorizer as ic,idlelib.percolator as ip,re;

class App:
# -------------------------- INITIALIZE APPLICATION
    def __init__(self) -> None:
        self.args=sys.argv
        if((len(self.args))>1 or not __file__.endswith((".py",".pyw"))and not "--light" in sys.argv):
            self.path=self.args[-1]
            if not os.path.exists(self.path):
                open(self.path,"a+",encoding="utf8").close()
            try:
                self.inittext=open(self.path).read()
            except:pass
        else:
            self.path=None
            self.inittext=""

        self.fontSize=12;
        self.codeActive=False;
        self.ip=None;
        QApplication(sys.argv)
        self.thread=thread.Thread(target=self.main)
    def updateTitle(self,*args) -> None:
        self.root.title(f"*{self.path} - WEdit")
# -------------------------- SAVE FILE HANDLER

    def save(self,*args):
        try:
            if self.path is None:
                self.saveas()
                return;
            open(self.path,"w",encoding="utf8").write(self.notepad.get("1.0","end-1c"))
            self.root.title(f"{self.path} - WEdit")
        except:pass    
    def saveas(self,*args):
        try:
            self.path=filedialog.asksaveasfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="save file",initialfile="untilted.txt").replace("\\","/")
            if self.path is not None:
                if self.path.endswith((".pyw","py",".c","cpp",".js",".java",".ts",".go",".asm",".h",".hpp",".html",".htm",".css")):
                    if not self.codeActive:self.syntaxSetter()
                self.save()
        except:pass
    
    def importfile(self,*args):
        try:
            path=filedialog.askopenfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="import file").replace("\\","/")
            if path is not None:
                if path.endswith((".pyw","py",".c","cpp",".js",".java",".ts",".go",".asm",".h",".hpp",".html",".htm",".css")):
                    self.syntaxSetter()
                self.notepad.insert(END,path)
        except:pass    
    
    def open(self,new:bool=False,*args):
        try:
            self.path=filedialog.askopenfilename(filetypes=[("Text file",".txt"),("Any file",".*"),("C source",".c"),("C++ source",".cpp"),("Java source",".java"),("JavaScript source",".js"),("TypeScript source",".ts"),("HTML source",".html"),("CSS source",".css"),("Assembly source",".asm"),("Python source",".py"),("Python consoleless source",".pyw"),],parent=self.root,title="open file").replace("\\","/")
            if self.path is not None:
                self.syntaxSetter()
                self.notepad.delete("1.0",END)
                self.notepad.insert(END,open(self.path,"r",encoding="utf8").read())
                self.save()
        except:pass
# -------------------------- SYNTAX HIGHLIGHTING STUFF
    def syntaxSetter(self,*args,**kwargs):
        if str(self.path).endswith((".c",".h",)):
            KEYWORD   = r"\b(?P<KEYWORD>do|while|for|if|switch|return|extern|struct|typedef|include|volatile|sizeof|static|const|union|case|default|enum|goto|register|break|continue|else)\b"
            BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abort|abs|acos|asctime|asctime_r|asin|assert|atan|atan2|atexit|atof|atoi|atol|bsearch|btowc|stdio|wchar|wint_t|calloc|catclose6|catgets6|catopen6|ceil|clearerr|clock|cos|cosh|ctime|ctime64|ctime_r|ctime64_r|difftime|difftime64|div|erf|erfc|exit|exp|fabs|fclose|fdopen5|feof|ferror|fflush1|fgetc1|fgetpos1|fgets1|fgetwc6|stdio|wchar|wint_t|fgetws6|stdio|wchar|wchar_t|fileno5|floor|fmod|fopen|fprintf|fputc1|fputs1|fputwc6|stdio|wchar|wint_t|fputws6|stdio|wchar|int|fread|free|freopen|frexp|fscanf|fseek1|fsetpos1|ftell1|fwide6|stdio|wchar|int|fwprintf6|stdio|wchar|int|fwrite|fwscanf6|stdio|wchar|int|gamma|getc1|getchar1|getenv|gets|getwc6|stdio|wchar|wint_t|getwchar6|gmtime|gmtime64|gmtime_r|gmtime64_r|hypot|isalnum|isalpha|isascii4|isblank|iscntrl|isdigit|isgraph|islower|isprint|ispunct|isspace|isupper|iswalnum4|iswalpha4|iswblank4|iswcntrl4|iswctype4|iswdigit4|iswgraph4|iswlower4|iswprint4|iswpunct4|iswspace4|iswupper4|iswxdigit4|isxdigit4|j0|j1|jn|labs|ldexp|ldiv|localeconv|localtime|localtime64|localtime_r|localtime64_r|log|log10|longjmp|malloc|mblen|mbrlen4|mbrtowc4|mbsinit4|mbsrtowcs4|mbstowcs|mbtowc|memchr|memcmp|memcpy|memmove|memset|mktime|mktime64|modf|nextafter|nextafterl|nexttoward|nexttowardl|nl_langinfo4|perror|pow|printf|putc1|putchar1|putenv|puts|putwc6|stdio|wchar|wint_t|putwchar6|qsort|quantexpd32|quantexpd64|quantexpd128|quantized32|quantized64|quantized128|samequantumd32|samequantumd64|samequantumd128|raise|rand|rand_r|realloc|regcomp|regerror|regexec|regfree|remove|rename|rewind1|scanf|setbuf|setjmp|setlocale|setvbuf|signal|sin|sinh|snprintf|sprintf|sqrt|srand|sscanf|strcasecmp|strcat|strchr|strcmp|strcoll|strcpy|strcspn|strerror|strfmon4|strftime|strlen|strncasecmp|strncat|strncmp|strncpy|strpbrk|strptime4|strrchr|strspn|strstr|strtod|strtod32|strtod64|strtod128|strtof|strtok|strtok_r|strtol|strtold|strtoul|strxfrm|swprintf|swscanf|system|tan|tanh|time|time64|tmpfile|tmpnam|toascii|tolower|toupper|towctrans|towlower4|towupper4|ungetc1|ungetwc6|stdio|wchar|wint_t|va_arg|va_copy|va_end|va_start|vfprintf|vfscanf|vfwprintf6|stdarg|stdio|wchar|int|vfwscanf|vprintf|vscanf|vsprintf|vsnprintf|vsscanf|vswprintf|stdarg|wchar|int|vswscanf|vwprintf6|stdarg|wchar|int|vwscanf|wcrtomb4|wcscat|wcschr|wcscmp|wcscoll4|wcscpy|wcscspn|wcsftime|wcslen|wcslocaleconv|wcsncat|wcsncmp|wcsncpy|wcspbrk|wcsptime|wcsrchr|wcsrtombs4|wcsspn|wcsstr|wcstod|wcstod32|wcstod64|wcstod128|wcstof|wcstok|wcstol|wcstold|wcstombs|wcstoul|wcsxfrm4|wctob|stdarg|wchar|int|wctomb|wctrans|wctype4|wcwidth|wmemchr|wmemcmp|wmemcpy|wmemmove|wmemset|wprintf6|wscanf6|y0|y1|yn)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{BUILTIN}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".hpp",".cpp",".c++")):
            KEYWORD   = r"\b(?P<KEYWORD>alignas|alignof|asm|auto|bool|break|case|catch|char|char8_t|char16_t|char32_t|class|concept|const|consteval|constexpr|constinit|const_cast|continue|co_await|co_return|co_yield|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|nullptr|operator|private|protected|public|register|reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|true|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|and|and_eq|bitand|bitor|compl|not|not_eq|or|or_eq|xor|xor_eq)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".dart")):
            KEYWORD   = r"\b(?P<KEYWORD>assert|break|case|catch|class|const|continue|default|do|else|enum|extends|false|final|finally|for|if|in|is|new|null|rethrow|return|super|switch|this|throw|true|try|var|void|while|with)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".f90",".for",".f")):
            KEYWORD   = r"\b(?P<KEYWORD>abstract|allocatable|allocate|assign|associate|asynchronous|backspace|bind|block|block data|call|case|class|close|codimension|common|contains|contiguous|continue|critical|cycle|data|deallocate|deferred|dimension|do|do concurrent|elemental|else|else if|elsewhere|end|endfile|endif|entry|enum|enumerator|equivalence|error stop|exit|extends|external|final|flush|forall|format|function|generic|goto|if|implicit|import|include|inquire|intent|interface|intrinsic|lock|module|namelist|non_overridable|nopass|nullify|only|open|operator|optional|parameter|pass|pause|pointer|print|private|procedure|program|protected|public|pure|read|recursive|result|return|rewind|rewrite|save|select|sequence|stop|submodule|subroutine|sync all|sync images|sync memory|target|then|unlock|use|value|volatile|wait|where|while|write)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".go",".golang")):
            KEYWORD   = r"\b(?P<KEYWORD>break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go|goto|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".java")):
            KEYWORD   = r"\b(?P<KEYWORD>abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|if|goto|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while|_)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".js")):
            KEYWORD   = r"\b(?P<KEYWORD>break|case|catch|class|const|continue|debugger|default|delete|do|else|export|extends|finally|for|function|if|import|in|instanceof|new|return|super|switch|this|throw|try|typeof|var|void|while|with|yield|let|static|enum|await|implements|interface|package|private|protected|public|null|true|false)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".kt", ".kts", ".ktm")):
            KEYWORD   = r"\b(?P<KEYWORD>as|break|class|continue|do|else|false|for|fun|if|in|interface|isis|null|object|package|return|super|this|throw|true|try|typealias|typeof|val|var|when|while|by|catch|constructor|delegate|dynamic|field|file|finally|get|import|init|param|property|receiver|set|setparam|where|actual|abstract|annotation|companion|const|crossinline|data|enum|expect|external|final|infix|inline|inner|internal|lateinit|noinline|open|operator|out|override|private|protected|public|reified|sealed|suspend|tailrec|vararg|field|it)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".m")):
            KEYWORD   = r"\b(?P<KEYWORD>asm|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|__block|Imaginary|id|Class|SEL|IMP|BOOL|nil|Nil|YES|NO|self|super|_cmd|__strong|__weak|__autoreleasing|__unsafe_unretained|oneway|In|out|inout|bycopy|byref)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".php")):
            KEYWORD   = r"\b(?P<KEYWORD>__halt_compiler\(\)|abstract|and|array\(\)|as|break|callable|case|catch|class|clone|const|continue|declare|default|die\(\)|do|echo|else|elseif|empty\(\)|enddeclare|endfor|endforeach|endif|endswitch|endwhile|eval\(\)|exit\(\)|extends|final|finally|fn|for|foreach|function|global|goto|if|implements|include|include_once|instanceof|insteadof|interface|isset\(\)|list\(\)|namespace|new|or|print|private|protected|public|require|require_once|return|static|switch|throw|trait|try|unset\(\)|use|var|while|xor|yield|yield from)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        elif str(self.path).endswith((".rs",".rslib")):
            KEYWORD   = r"\b(?P<KEYWORD>associatedtype|class|deinit|enum|extension|fileprivate|func|import|init|inout|internal|let|open|operator|private|protocol|public|rethrows|static|struct|subscript|typealias|var|break|case|continue|default|defer|do|else|fallthrough|for|guard|if|in|repeat|return|switch|where|while|as|Any|catch|false|is|nil|super|self|Self|throw|throws|true|try|_|#available|#colorLiteral|#column|#else|#elseif|#endif|#error|#file|#filePath|#fileLiteral|#function|#if|#imageLiteral|#line|#selector|#sourceLocation|#warning|associativity|convenience|dynamic|didSet|final|get|infix|indirect|lazy|left|mutating|none|nonmutating|optional|override|postfix|precedence|prefix|Protocol|required|right|set|Type|unowned|weak|willSet)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        
        elif str(self.path).endswith((".lua")):
            KEYWORD   = r"\b(?P<KEYWORD>and|break|do|else|elseif|end|false|for|function|goto|if|in|local|nil|not|or|repeat|return|then|true|until|while)\b"
            STRING    = r"(?P<STRING>()?'[^'\\\n]*(\\.[^'\\\n]*)*'?|()?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>char|int|double|float|long|short|unsigned|auto|void)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            COMMENT   = r"(?P<COMMENT>[//][^\n]*|[/*]+[*/])"
            SYNC      = r"(?P<SYNC>\n)"
            SYMBOLS   = r"(?P<SYMBOLS>(\+|[^\/]\*|\||\&|\%|\-|\#|\/[^\/|^\*]))"
            PROG   = rf"{SYMBOLS}|{KEYWORD}|{TYPES}|{COMMENT}|{STRING}|{SYNC}|{NUMBER}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   
                            'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#8f2d24',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'ANYFUNC'    : {'foreground': '#8f2d24',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'SYMBOLS'    : {'foreground': '#28b9c9',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                        }
        
        elif str(self.path).endswith((".py",".pyw",".xonshrc",".xsh")):
            KEYWORD   = r"\b(?P<KEYWORD>False|None|True|true|false|public|static|and|as|assert|void|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
            EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b"
            BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|printf|scanf|cout|cin|System|println|mov|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b"
            DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
            STRING    = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object|char|double)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            CLASSDEF  = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]" #recolor of DEFINITION for class definitions
            DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
            INSTANCE  = r"\b(?P<INSTANCE>super|self|cls)\b"
            COMMENT   = r"(?P<COMMENT>#|//[^\n]*)"
            SYNC      = r"(?P<SYNC>\n)"
            PROG   = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   'COMMENT'    : {'foreground': '#333333',    'background': None},
                            'TYPES'      : {'foreground': '#c70a0a',    'background': None},
                            'NUMBER'     : {'foreground': '#28b9c9',    'background': None},
                            'BUILTIN'    : {'foreground': '#f04b05',    'background': None},
                            'STRING'     : {'foreground': '#28b9c9',    'background': None},
                            'DOCSTRING'  : {'foreground': '#28b9c9',    'background': None},
                            'EXCEPTION'  : {'foreground': '#e00914',    'background': None},
                            'DEFINITION' : {'foreground': '#44ab1b',    'background': None},
                            'DECORATOR'  : {'foreground': '#994f2c',    'background': None},
                            'INSTANCE'   : {'foreground': '#706b1e',    'background': None},
                            'KEYWORD'    : {'foreground': '#b00914',    'background': None},
                            'CLASSDEF'   : {'foreground': '#c97f1e',    'background': None},
                        }
        else:
            KEYWORD   = r"\b(?P<KEYWORD>False|None|True|true|false|public|static|and|as|assert|void|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
            EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b"
            BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|printf|scanf|cout|cin|System|println|mov|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b"
            DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
            STRING    = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
            TYPES     = r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object|char|double)\b"
            NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
            CLASSDEF  = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]" #recolor of DEFINITION for class definitions
            DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
            INSTANCE  = r"\b(?P<INSTANCE>super|self|cls)\b"
            COMMENT   = r"(?P<COMMENT>#|//[^\n]*)"
            SYNC      = r"(?P<SYNC>\n)"
            PROG   = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"
            IDPROG = r"(?<!class)\s+(\w+)"
            TAGDEFS   = {   'COMMENT'    : {'foreground': '#fff',    'background': None},
                            'TYPES'      : {'foreground': '#fff',    'background': None},
                            'NUMBER'     : {'foreground': '#fff',    'background': None},
                            'BUILTIN'    : {'foreground': '#fff',    'background': None},
                            'STRING'     : {'foreground': '#fff',    'background': None},
                            'DOCSTRING'  : {'foreground': '#fff',    'background': None},
                            'EXCEPTION'  : {'foreground': '#fff',    'background': None},
                            'DEFINITION' : {'foreground': '#fff',    'background': None},
                            'DECORATOR'  : {'foreground': '#fff',    'background': None},
                            'INSTANCE'   : {'foreground': '#fff',    'background': None},
                            'KEYWORD'    : {'foreground': '#fff',    'background': None},
                            'CLASSDEF'   : {'foreground': '#fff',    'background': None},
                        }
        cd         = ic.ColorDelegator()
        cd.prog    = re.compile(PROG, re.S|re.M)
        cd.idprog  = re.compile(IDPROG, re.S)
        cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
        if self.ip is None:
            self.ip=ip.Percolator(self.notepad)

        if self.codeActive:
            cd.tagdefs = TAGDEFS
        self.ip.insertfilter(cd)
        self.codeActive = not self.codeActive
# -------------------------- DARK TITLE BAR
    def darkTitleBar(self):
        """
        MORE INFO:
        https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """
        try:
            self.root.update()
            if os.name=="nt":
                ct.windll.dwmapi.DwmSetWindowAttribute(
                    ct.windll.user32.GetParent(
                        self.root.winfo_id()
                    ), 
                    20, 
                    ct.byref(
                        ct.c_int(2)
                    ),
                    ct.sizeof(
                        ct.c_int(2)
                    )
                )
        except:pass
# -------------------------- START APP
    def start(self):
        self.thread.start();
# -------------------------- CLOSE APP
    def close(self,*args,**kwargs):
        if self.path is not None:
            self.save()
        self.root.withdraw();
        sys.exit(0);
# -------------------------- NEGATIVIZE COLORS OF ANY IMAGE
    def invert(self,image:Image.Image):
        if image.mode == 'RGBA':
            r,g,b,a = image.split()
            rgb_image = Image.merge('RGB', (r,g,b))

            inverted_image = ImageOps.invert(rgb_image)

            r2,g2,b2 = inverted_image.split()

            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))

            return final_transparent_image
        else:
            inverted_image = ImageOps.invert(image)
            return inverted_image
    def increaseFont(self,*args,**kwargs):
        self.fontSize+=1
        self.notepad.configure(font=f"Courier {self.fontSize}")
    def decreaseFont(self,*args,**kwargs):
        if self.fontSize<5:
            return;
        self.fontSize-=1
        self.notepad.configure(font=f"Courier {self.fontSize}")
# -------------------------- CONFIGURE ROOT SETTINGS AND PROPERTIES
    def configure(self):
        self.root.protocol("WM_DELETE_WINDOW",self.close)#Protocol for closing
        self.root.bind("<Control-w>",self.close)#Shortcut (like exporer or google chrome)
        self.root.bind("<Control-+>",self.increaseFont)
        self.root.bind("<Control-minus>",self.decreaseFont)
        self.root.bind("<Control-s>",self.save)
        self.root.bind("<Control-Shift-S>",self.saveas)
        self.root.bind("<Control-o>",self.open)
        self.root.bind("<Control-Shift-O>",self.importfile)
        self.root.bind("<Control-t>",self.timeIn)
        self.root.bind("<Key>",self.updateTitle)
        

        #root size
        self.root.geometry("%dx%d"%(self.root.winfo_screenwidth()/2.5,self.root.winfo_screenheight()/2.5))
        
        #title
        self.root.title("Untilted - WEdit")

        #upscale to 2x
        self.root.tk.call('tk', 'scaling',2)
        
        #set dark theme things (icons,theme)
        if d.isDark() and "--light" not in sys.argv:
            self.darkTitleBar()
            SetStyle.set_theme("dark")
            self.images={
                "open":ImageTk.PhotoImage(self.invert(Image.open("./assets/open.png")).resize([20,20])),
                "file":ImageTk.PhotoImage(self.invert(Image.open("./assets/menu.png")).resize([20,20])),
                "save":ImageTk.PhotoImage(self.invert(Image.open("./assets/save.png").resize([20,20]))),
                "saveas":ImageTk.PhotoImage(self.invert(Image.open("./assets/saveas.png").resize([20,20]))),
                "add":ImageTk.PhotoImage(self.invert(Image.open("./assets/add.png").resize([20,20]))),
                "find":ImageTk.PhotoImage(self.invert(Image.open("./assets/find.png").resize([20,20]))),
                "findnext":ImageTk.PhotoImage(self.invert(Image.open("./assets/findnext.png").resize([20,20]))),
                "findprev":ImageTk.PhotoImage(self.invert(Image.open("./assets/findprev.png").resize([20,20]))),
                "redo":ImageTk.PhotoImage(self.invert(Image.open("./assets/redo.png").resize([20,20]))),
                "undo":ImageTk.PhotoImage(self.invert(Image.open("./assets/undo.png").resize([20,20]))),
                "copy":ImageTk.PhotoImage(self.invert(Image.open("./assets/copy.png").resize([20,20]))),
                "cut":ImageTk.PhotoImage(self.invert(Image.open("./assets/cut.png").resize([20,20]))),
                "delete":ImageTk.PhotoImage(self.invert(Image.open("./assets/delete.png").resize([20,20]))),
                "goto":ImageTk.PhotoImage(self.invert(Image.open("./assets/goto.png").resize([20,20]))),
                "select":ImageTk.PhotoImage(self.invert(Image.open("./assets/select.png").resize([20,20]))),
                "date":ImageTk.PhotoImage(self.invert(Image.open("./assets/date.png").resize([20,20]))),
                "code":ImageTk.PhotoImage(self.invert(Image.open("./assets/code.png").resize([20,20]))),
            }
        else:
            self.images={
                "open":ImageTk.PhotoImage(Image.open("./assets/open.png").resize([20,20])),
                "file":ImageTk.PhotoImage(Image.open("./assets/menu.png").resize([20,20])),
                "save":ImageTk.PhotoImage(Image.open("./assets/save.png").resize([20,20])),
                "saveas":ImageTk.PhotoImage(Image.open("./assets/saveas.png").resize([20,20])),
                "add":ImageTk.PhotoImage(Image.open("./assets/add.png").resize([20,20])),
                "find":ImageTk.PhotoImage(Image.open("./assets/find.png").resize([20,20])),
                "findnext":ImageTk.PhotoImage(Image.open("./assets/findnext.png").resize([20,20])),
                "findprev":ImageTk.PhotoImage(Image.open("./assets/findprev.png").resize([20,20])),
                "redo":ImageTk.PhotoImage(Image.open("./assets/redo.png").resize([20,20])),
                "undo":ImageTk.PhotoImage(Image.open("./assets/undo.png").resize([20,20])),
                "copy":ImageTk.PhotoImage(Image.open("./assets/copy.png").resize([20,20])),
                "cut":ImageTk.PhotoImage(Image.open("./assets/cut.png").resize([20,20])),
                "delete":ImageTk.PhotoImage(Image.open("./assets/delete.png").resize([20,20])),
                "goto":ImageTk.PhotoImage(Image.open("./assets/goto.png").resize([20,20])),
                "select":ImageTk.PhotoImage(Image.open("./assets/select.png").resize([20,20])),
                "date":ImageTk.PhotoImage(Image.open("./assets/date.png").resize([20,20])),
                "code":ImageTk.PhotoImage(Image.open("./assets/code.png").resize([20,20])),
            }
            SetStyle.set_theme("light")
# -------------------------- DATETIME
    def timeIn(self, *args):
        self.notepad.insert(END,"%s\n"%(datetime.now().strftime("%D %T")))
# -------------------------- CUT TEXT
    def cut(self):
        pyperclip.copy(self.notepad.selection_get())
        self.notepad.selection_clear()
    def undo(self):
        self.notepad.edit_undo()
    def redo(self):
        self.notepad.edit_redo()
# -------------------------- TOP MENU BAR BUILT FROM SCRATCH
    def menubar(self):
        self.topbar=Frame(self.root)
        self.topbar.pack(side=TOP,fill=X)


        self.menu1=Menu(self.root)
        self.menu1.add_command(label="Open",accelerator="Ctrl+O",underline=0,image=self.images.get("open"),command=self.open,compound="left")
        self.menu1.add_command(label="Import text",accelerator="Ctrl+Shift+O",underline=0,image=self.images.get("add"),command=self.importfile,compound="left")
        self.menu1.add_separator()
        self.menu1.add_command(label="Save",accelerator="Ctrl+S",underline=0,image=self.images.get("save"),command=self.save,compound="left")
        self.menu1.add_command(label="Save As",accelerator="Ctrl+Shift+S",underline=0,image=self.images.get("saveas"),command=self.saveas,compound="left")
        
        self.MenuButton1=Menubutton(self.topbar,text="File",menu=self.menu1,image=self.images.get("file"),compound="left")
        self.MenuButton1.pack(side=LEFT)

        self.menu2=Menu(self.root)
        self.root.bind("<Control-Shift-C>",self.syntaxSetter)
        self.menu2.add_command(label="Code Highlighting",accelerator="Ctrl+Shift+C",command=self.syntaxSetter,underline=0,image=self.images.get("code"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Find",accelerator="Ctrl+F",underline=0,image=self.images.get("find"),compound="left")
        self.menu2.add_command(label="Find Next",accelerator="Ctrl+Shift+F",underline=0,image=self.images.get("findnext"),compound="left")
        self.menu2.add_command(label="Find Previous",accelerator="Ctrl+Alt+F",underline=0,image=self.images.get("findprev"),compound="left")
        self.menu2.add_command(label="Go to",accelerator="Ctrl+G",underline=0,image=self.images.get("goto"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Undo",accelerator="Ctrl+Z",command=self.undo,underline=0,image=self.images.get("undo"),compound="left")
        self.menu2.add_command(label="Redo",accelerator="Ctrl+Y",command=self.redo,underline=0,image=self.images.get("redo"),compound="left")
        self.menu2.add_separator()
        self.menu2.add_command(label="Copy",accelerator="Ctrl+C",command=lambda:pyperclip.copy(self.notepad.selection_get()),underline=0,image=self.images.get("copy"),compound="left")
        self.menu2.add_command(label="Cut",accelerator="Ctrl+X",command=self.cut,underline=0,image=self.images.get("cut"),compound="left")
        self.menu2.add_command(label="Select all",accelerator="Ctrl+A",underline=0,image=self.images.get("select"),compound="left")
        self.menu2.add_command(label="Delete",accelerator="Canc",underline=0,image=self.images.get("delete"),compound="left")

        self.MenuButton2=Menubutton(self.topbar,text="Modify",menu=self.menu2,image=self.images.get("file"),compound="left")
        self.MenuButton2.pack(side=LEFT)

        self.menu3=Menu(self.root)
        self.menu3.add_command(label="Date and Time",command=self.timeIn,accelerator="Ctrl+T",underline=0,image=self.images.get("date"),compound="left")

        self.MenuButton3=Menubutton(self.topbar,text="Insert",menu=self.menu3,image=self.images.get("file"),compound="left")
        self.MenuButton3.pack(side=LEFT)

        self.root.update()
    
    def get(self,arr,key):
        try:
            return arr[key]
        except:
            return "";
    
    def indent(self,*args,**kwargs):
        # kinda buggy for now not implemented
        # if self.codeActive:
        #     o_=self.notepad.get("1.0","end-1c")
        #     o2_=self.get(o_.splitlines(),-1)
        #     self.notepad.insert(END,"\t"*o2_.count("\t"))
        #     self.notepad.update()
        #     return
        return

    def textbox(self):
        self.notepad=Text(self.root,font=f"Courier {self.fontSize}",maxundo=-1,undo=True)
        self.notepad.pack(side=TOP,fill=BOTH,expand=True)
        self.notepad.bind("<Return>",self.indent)
        self.notepad.insert(END,self.inittext)
    def main(self):
        self.root=Tk();

        self.configure();

        self.menubar();

        self.textbox();

        #Some bottom colorings (win only)
        Progressbar(self.root,value=100).pack(side=BOTTOM)

        self.root.mainloop();

if __name__=="__main__":
    app=App()
    app.start()