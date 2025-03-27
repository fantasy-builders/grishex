"""
Grishex - Синтаксический анализатор

Модуль для преобразования токенов Grishex в абстрактное синтаксическое дерево (AST).
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum, auto
from lexer import Token, TokenType


class ASTNodeType(Enum):
    """Типы узлов для абстрактного синтаксического дерева."""
    # Основные конструкции
    PROGRAM = auto()          # Программа
    PRAGMA = auto()           # Прагма
    CONTRACT = auto()         # Контракт
    INTERFACE = auto()        # Интерфейс
    STATE = auto()            # Состояние
    CONSTRUCTOR = auto()      # Конструктор
    FUNCTION = auto()         # Функция
    EVENT = auto()            # Событие
    STRUCT = auto()           # Структура
    ENUM = auto()             # Перечисление
    
    # Выражения
    BINARY_EXPR = auto()      # Бинарное выражение
    UNARY_EXPR = auto()       # Унарное выражение
    LITERAL = auto()          # Литерал
    IDENTIFIER = auto()       # Идентификатор
    MEMBER_ACCESS = auto()    # Доступ к члену (foo.bar)
    INDEX_ACCESS = auto()     # Доступ по индексу (foo[bar])
    CALL_EXPR = auto()        # Вызов функции
    
    # Операторы
    BLOCK = auto()            # Блок кода
    VAR_DECLARATION = auto()  # Объявление переменной
    ASSIGNMENT = auto()       # Присваивание
    IF_STMT = auto()          # Условный оператор
    WHILE_STMT = auto()       # Цикл while
    FOR_STMT = auto()         # Цикл for
    FOREACH_STMT = auto()     # Цикл foreach
    RETURN_STMT = auto()      # Оператор return
    REQUIRE_STMT = auto()     # Оператор require
    ASSERT_STMT = auto()      # Оператор assert
    REVERT_STMT = auto()      # Оператор revert
    EMIT_STMT = auto()        # Оператор emit
    TRY_CATCH_STMT = auto()   # Блок try-catch
    
    # Типы данных
    TYPE = auto()             # Тип данных
    PARAM = auto()            # Параметр функции
    PARAM_LIST = auto()       # Список параметров


class ASTNode:
    """Базовый класс для узлов AST."""
    
    def __init__(self, node_type: ASTNodeType, **kwargs):
        """
        Инициализирует узел AST.
        
        Args:
            node_type: Тип узла
            **kwargs: Дополнительные атрибуты узла
        """
        self.node_type = node_type
        self.attributes = kwargs
        self.children = []
    
    def add_child(self, child: 'ASTNode') -> None:
        """
        Добавляет дочерний узел.
        
        Args:
            child: Дочерний узел
        """
        self.children.append(child)
    
    def set_attribute(self, name: str, value: Any) -> None:
        """
        Устанавливает атрибут узла.
        
        Args:
            name: Имя атрибута
            value: Значение атрибута
        """
        self.attributes[name] = value
    
    def get_attribute(self, name: str, default: Any = None) -> Any:
        """
        Получает значение атрибута.
        
        Args:
            name: Имя атрибута
            default: Значение по умолчанию, если атрибут не найден
            
        Returns:
            Значение атрибута или default, если атрибут не найден
        """
        return self.attributes.get(name, default)
    
    def __repr__(self) -> str:
        """
        Возвращает строковое представление узла.
        
        Returns:
            Строковое представление узла
        """
        return f"ASTNode({self.node_type}, {self.attributes})"


class ParserError(Exception):
    """Исключение, возникающее при ошибке синтаксического анализа."""
    
    def __init__(self, token: Token, message: str):
        """
        Инициализирует исключение.
        
        Args:
            token: Токен, на котором произошла ошибка
            message: Сообщение об ошибке
        """
        self.token = token
        self.message = message
        super().__init__(f"Error at line {token.line}, column {token.column}: {message}")


class Parser:
    """Синтаксический анализатор для Grishex."""
    
    def __init__(self, tokens: List[Token]):
        """
        Инициализирует синтаксический анализатор.
        
        Args:
            tokens: Список токенов для анализа
        """
        self.tokens = tokens
        self.current = 0
        self.errors = []
    
    def parse(self) -> ASTNode:
        """
        Выполняет синтаксический анализ и строит AST.
        
        Returns:
            Корень AST
        """
        try:
            return self._parse_program()
        except ParserError as e:
            self.errors.append(e)
            return ASTNode(ASTNodeType.PROGRAM)
    
    def _advance(self) -> Token:
        """
        Переходит к следующему токену.
        
        Returns:
            Предыдущий токен
        """
        token = self.tokens[self.current]
        self.current += 1
        return token
    
    def _peek(self, offset: int = 0) -> Token:
        """
        Возвращает токен на заданном смещении от текущей позиции.
        
        Args:
            offset: Смещение
            
        Returns:
            Токен
        """
        if self.current + offset >= len(self.tokens):
            return self.tokens[-1]  # Возвращаем последний токен (EOF)
        return self.tokens[self.current + offset]
    
    def _check(self, token_type: TokenType) -> bool:
        """
        Проверяет, соответствует ли текущий токен заданному типу.
        
        Args:
            token_type: Тип токена
            
        Returns:
            True, если типы совпадают, иначе False
        """
        if self._is_at_end():
            return False
        return self._peek().type == token_type
    
    def _match(self, *token_types: TokenType) -> bool:
        """
        Проверяет, соответствует ли текущий токен одному из заданных типов.
        Если соответствует, переходит к следующему токену.
        
        Args:
            token_types: Типы токенов
            
        Returns:
            True, если типы совпадают, иначе False
        """
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """
        Проверяет, соответствует ли текущий токен заданному типу.
        Если соответствует, переходит к следующему токену, иначе генерирует ошибку.
        
        Args:
            token_type: Тип токена
            message: Сообщение об ошибке
            
        Returns:
            Текущий токен
        """
        if self._check(token_type):
            return self._advance()
        
        raise ParserError(self._peek(), message)
    
    def _is_at_end(self) -> bool:
        """
        Проверяет, достигнут ли конец списка токенов.
        
        Returns:
            True, если достигнут конец, иначе False
        """
        return self._peek().type == TokenType.EOF
    
    def _parse_program(self) -> ASTNode:
        """
        Разбирает программу.
        
        Returns:
            Узел программы
        """
        # Создаем корневой узел
        program = ASTNode(ASTNodeType.PROGRAM)
        
        # Разбираем прагму, если она есть
        if self._match(TokenType.PRAGMA):
            program.add_child(self._parse_pragma())
        
        # Разбираем объявления (контракты, интерфейсы и т.д.)
        while not self._is_at_end():
            if self._match(TokenType.CONTRACT):
                program.add_child(self._parse_contract())
            elif self._match(TokenType.INTERFACE):
                program.add_child(self._parse_interface())
            elif self._match(TokenType.STRUCT):
                program.add_child(self._parse_struct())
            elif self._match(TokenType.ENUM):
                program.add_child(self._parse_enum())
            else:
                # Неожиданный токен
                raise ParserError(self._peek(), f"Unexpected token: {self._peek().value}")
        
        return program
    
    def _parse_pragma(self) -> ASTNode:
        """
        Разбирает прагму.
        
        Returns:
            Узел прагмы
        """
        # Ожидаем, что следующий токен - идентификатор (grishex)
        identifier = self._consume(TokenType.IDENTIFIER, "Expected 'grishex' after 'pragma'")
        
        # Проверяем, что идентификатор - 'grishex'
        if identifier.value != 'grishex':
            raise ParserError(identifier, f"Expected 'grishex', got '{identifier.value}'")
        
        # Ожидаем версию
        version = self._consume(TokenType.INTEGER, "Expected version number after 'grishex'")
        
        # Ожидаем точку с запятой
        self._consume(TokenType.SEMICOLON, "Expected ';' after pragma declaration")
        
        # Создаем узел прагмы
        pragma = ASTNode(ASTNodeType.PRAGMA, name='grishex', version=version.value)
        
        return pragma
    
    def _parse_contract(self) -> ASTNode:
        """
        Разбирает контракт.
        
        Returns:
            Узел контракта
        """
        # Ожидаем имя контракта
        name = self._consume(TokenType.IDENTIFIER, "Expected contract name")
        
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' after contract name")
        
        # Создаем узел контракта
        contract = ASTNode(ASTNodeType.CONTRACT, name=name.value)
        
        # Разбираем содержимое контракта
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            if self._match(TokenType.STATE):
                contract.add_child(self._parse_state())
            elif self._match(TokenType.CONSTRUCTOR):
                contract.add_child(self._parse_constructor())
            elif self._match(TokenType.FUNCTION):
                contract.add_child(self._parse_function(is_view=False))
            elif self._match(TokenType.VIEW):
                self._consume(TokenType.FUNCTION, "Expected 'function' after 'view'")
                contract.add_child(self._parse_function(is_view=True))
            elif self._match(TokenType.PRIVATE):
                self._consume(TokenType.FUNCTION, "Expected 'function' after 'private'")
                contract.add_child(self._parse_function(is_private=True))
            elif self._match(TokenType.EVENT):
                contract.add_child(self._parse_event())
            else:
                # Неожиданный токен
                raise ParserError(self._peek(), f"Unexpected token in contract: {self._peek().value}")
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' after contract definition")
        
        return contract
    
    def _parse_interface(self) -> ASTNode:
        """
        Разбирает интерфейс.
        
        Returns:
            Узел интерфейса
        """
        # Ожидаем имя интерфейса
        name = self._consume(TokenType.IDENTIFIER, "Expected interface name")
        
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' after interface name")
        
        # Создаем узел интерфейса
        interface = ASTNode(ASTNodeType.INTERFACE, name=name.value)
        
        # Разбираем содержимое интерфейса
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            if self._match(TokenType.FUNCTION):
                interface.add_child(self._parse_function_signature())
            elif self._match(TokenType.VIEW):
                self._consume(TokenType.FUNCTION, "Expected 'function' after 'view'")
                interface.add_child(self._parse_function_signature(is_view=True))
            elif self._match(TokenType.EVENT):
                interface.add_child(self._parse_event())
            else:
                # Неожиданный токен
                raise ParserError(self._peek(), f"Unexpected token in interface: {self._peek().value}")
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' after interface definition")
        
        return interface
    
    def _parse_state(self) -> ASTNode:
        """
        Разбирает блок состояния.
        
        Returns:
            Узел состояния
        """
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' after 'state'")
        
        # Создаем узел состояния
        state = ASTNode(ASTNodeType.STATE)
        
        # Разбираем переменные состояния
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            # Ожидаем имя переменной
            name = self._consume(TokenType.IDENTIFIER, "Expected variable name")
            
            # Ожидаем двоеточие
            self._consume(TokenType.COLON, "Expected ':' after variable name")
            
            # Разбираем тип
            type_node = self._parse_type()
            
            # Ожидаем точку с запятой
            self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
            
            # Создаем узел объявления переменной
            var_declaration = ASTNode(ASTNodeType.VAR_DECLARATION, name=name.value)
            var_declaration.add_child(type_node)
            
            # Добавляем узел объявления переменной в состояние
            state.add_child(var_declaration)
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' after state definition")
        
        return state
    
    def _parse_type(self) -> ASTNode:
        """
        Разбирает тип.
        
        Returns:
            Узел типа
        """
        # Проверяем, является ли текущий токен примитивным типом
        primitive_types = [
            TokenType.TYPE_INT, TokenType.TYPE_UINT, TokenType.TYPE_BOOL,
            TokenType.TYPE_ADDRESS, TokenType.TYPE_STRING, TokenType.TYPE_BYTES,
            TokenType.TYPE_HASH
        ]
        
        if self._match(*primitive_types):
            type_name = self.tokens[self.current - 1].value
            return ASTNode(ASTNodeType.TYPE, name=type_name)
        
        # Проверяем, является ли тип массивом
        if self._match(TokenType.TYPE_ARRAY):
            # Ожидаем открывающую угловую скобку
            self._consume(TokenType.LANGLE, "Expected '<' after 'array'")
            
            # Разбираем тип элементов массива
            element_type = self._parse_type()
            
            # Ожидаем закрывающую угловую скобку
            self._consume(TokenType.RANGLE, "Expected '>' after element type")
            
            # Создаем узел типа массива
            array_type = ASTNode(ASTNodeType.TYPE, name='array')
            array_type.add_child(element_type)
            
            return array_type
        
        # Проверяем, является ли тип отображением
        if self._match(TokenType.TYPE_MAP):
            # Ожидаем открывающую угловую скобку
            self._consume(TokenType.LANGLE, "Expected '<' after 'map'")
            
            # Разбираем тип ключа
            key_type = self._parse_type()
            
            # Ожидаем запятую
            self._consume(TokenType.COMMA, "Expected ',' after key type")
            
            # Разбираем тип значения
            value_type = self._parse_type()
            
            # Ожидаем закрывающую угловую скобку
            self._consume(TokenType.RANGLE, "Expected '>' after value type")
            
            # Создаем узел типа отображения
            map_type = ASTNode(ASTNodeType.TYPE, name='map')
            map_type.add_child(key_type)
            map_type.add_child(value_type)
            
            return map_type
        
        # Если ничего не подошло, ожидаем идентификатор
        identifier = self._consume(TokenType.IDENTIFIER, "Expected type name")
        
        return ASTNode(ASTNodeType.TYPE, name=identifier.value)
    
    def _parse_constructor(self) -> ASTNode:
        """
        Разбирает конструктор.
        
        Returns:
            Узел конструктора
        """
        # Ожидаем открывающую круглую скобку
        self._consume(TokenType.LPAREN, "Expected '(' after 'constructor'")
        
        # Разбираем параметры
        params = self._parse_parameters()
        
        # Ожидаем закрывающую круглую скобку
        self._consume(TokenType.RPAREN, "Expected ')' after constructor parameters")
        
        # Разбираем тело конструктора
        body = self._parse_block()
        
        # Создаем узел конструктора
        constructor = ASTNode(ASTNodeType.CONSTRUCTOR)
        
        # Добавляем параметры
        for param in params:
            constructor.add_child(param)
        
        # Добавляем тело
        constructor.add_child(body)
        
        return constructor
    
    def _parse_function(self, is_view: bool = False, is_private: bool = False) -> ASTNode:
        """
        Разбирает функцию.
        
        Args:
            is_view: Является ли функция представлением (view)
            is_private: Является ли функция приватной
            
        Returns:
            Узел функции
        """
        # Ожидаем имя функции
        name = self._consume(TokenType.IDENTIFIER, "Expected function name")
        
        # Ожидаем открывающую круглую скобку
        self._consume(TokenType.LPAREN, "Expected '(' after function name")
        
        # Разбираем параметры
        params = self._parse_parameters()
        
        # Ожидаем закрывающую круглую скобку
        self._consume(TokenType.RPAREN, "Expected ')' after function parameters")
        
        # Проверяем, есть ли возвращаемый тип
        return_type = None
        if self._match(TokenType.RETURNS):
            return_type = self._parse_type()
        
        # Разбираем тело функции
        body = self._parse_block()
        
        # Создаем узел функции
        function = ASTNode(ASTNodeType.FUNCTION, name=name.value, is_view=is_view, is_private=is_private)
        
        # Добавляем параметры
        for param in params:
            function.add_child(param)
        
        # Добавляем возвращаемый тип
        if return_type:
            function.set_attribute('return_type', return_type)
        
        # Добавляем тело
        function.add_child(body)
        
        return function
    
    def _parse_function_signature(self, is_view: bool = False) -> ASTNode:
        """
        Разбирает сигнатуру функции (для интерфейсов).
        
        Args:
            is_view: Является ли функция представлением (view)
            
        Returns:
            Узел функции
        """
        # Ожидаем имя функции
        name = self._consume(TokenType.IDENTIFIER, "Expected function name")
        
        # Ожидаем открывающую круглую скобку
        self._consume(TokenType.LPAREN, "Expected '(' after function name")
        
        # Разбираем параметры
        params = self._parse_parameters()
        
        # Ожидаем закрывающую круглую скобку
        self._consume(TokenType.RPAREN, "Expected ')' after function parameters")
        
        # Проверяем, есть ли возвращаемый тип
        return_type = None
        if self._match(TokenType.RETURNS):
            return_type = self._parse_type()
        
        # Ожидаем точку с запятой
        self._consume(TokenType.SEMICOLON, "Expected ';' after function signature")
        
        # Создаем узел функции
        function = ASTNode(ASTNodeType.FUNCTION, name=name.value, is_view=is_view, is_signature=True)
        
        # Добавляем параметры
        for param in params:
            function.add_child(param)
        
        # Добавляем возвращаемый тип
        if return_type:
            function.set_attribute('return_type', return_type)
        
        return function
    
    def _parse_parameters(self) -> List[ASTNode]:
        """
        Разбирает список параметров.
        
        Returns:
            Список узлов параметров
        """
        params = []
        
        # Если следующий токен - закрывающая скобка, значит параметров нет
        if self._check(TokenType.RPAREN):
            return params
        
        # Разбираем первый параметр
        params.append(self._parse_parameter())
        
        # Разбираем остальные параметры
        while self._match(TokenType.COMMA):
            params.append(self._parse_parameter())
        
        return params
    
    def _parse_parameter(self) -> ASTNode:
        """
        Разбирает параметр.
        
        Returns:
            Узел параметра
        """
        # Ожидаем имя параметра
        name = self._consume(TokenType.IDENTIFIER, "Expected parameter name")
        
        # Ожидаем двоеточие
        self._consume(TokenType.COLON, "Expected ':' after parameter name")
        
        # Разбираем тип параметра
        type_node = self._parse_type()
        
        # Создаем узел параметра
        param = ASTNode(ASTNodeType.PARAM, name=name.value)
        param.add_child(type_node)
        
        return param
    
    def _parse_event(self) -> ASTNode:
        """
        Разбирает событие.
        
        Returns:
            Узел события
        """
        # Ожидаем имя события
        name = self._consume(TokenType.IDENTIFIER, "Expected event name")
        
        # Ожидаем открывающую круглую скобку
        self._consume(TokenType.LPAREN, "Expected '(' after event name")
        
        # Разбираем параметры
        params = self._parse_parameters()
        
        # Ожидаем закрывающую круглую скобку
        self._consume(TokenType.RPAREN, "Expected ')' after event parameters")
        
        # Ожидаем точку с запятой
        self._consume(TokenType.SEMICOLON, "Expected ';' after event declaration")
        
        # Создаем узел события
        event = ASTNode(ASTNodeType.EVENT, name=name.value)
        
        # Добавляем параметры
        for param in params:
            event.add_child(param)
        
        return event
    
    def _parse_struct(self) -> ASTNode:
        """
        Разбирает структуру.
        
        Returns:
            Узел структуры
        """
        # Ожидаем имя структуры
        name = self._consume(TokenType.IDENTIFIER, "Expected struct name")
        
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' after struct name")
        
        # Создаем узел структуры
        struct = ASTNode(ASTNodeType.STRUCT, name=name.value)
        
        # Разбираем поля структуры
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            # Ожидаем имя поля
            field_name = self._consume(TokenType.IDENTIFIER, "Expected field name")
            
            # Ожидаем двоеточие
            self._consume(TokenType.COLON, "Expected ':' after field name")
            
            # Разбираем тип поля
            field_type = self._parse_type()
            
            # Ожидаем точку с запятой
            self._consume(TokenType.SEMICOLON, "Expected ';' after field declaration")
            
            # Создаем узел поля
            field = ASTNode(ASTNodeType.VAR_DECLARATION, name=field_name.value)
            field.add_child(field_type)
            
            # Добавляем поле в структуру
            struct.add_child(field)
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' after struct definition")
        
        return struct
    
    def _parse_enum(self) -> ASTNode:
        """
        Разбирает перечисление.
        
        Returns:
            Узел перечисления
        """
        # Ожидаем имя перечисления
        name = self._consume(TokenType.IDENTIFIER, "Expected enum name")
        
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' after enum name")
        
        # Создаем узел перечисления
        enum = ASTNode(ASTNodeType.ENUM, name=name.value)
        
        # Разбираем значения перечисления
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            # Ожидаем имя значения
            value_name = self._consume(TokenType.IDENTIFIER, "Expected enum value name")
            
            # Создаем узел значения
            value = ASTNode(ASTNodeType.IDENTIFIER, name=value_name.value)
            
            # Добавляем значение в перечисление
            enum.add_child(value)
            
            # Если следующий токен - запятая, пропускаем ее
            self._match(TokenType.COMMA)
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' after enum definition")
        
        return enum
    
    def _parse_block(self) -> ASTNode:
        """
        Разбирает блок кода.
        
        Returns:
            Узел блока
        """
        # Ожидаем открывающую фигурную скобку
        self._consume(TokenType.LBRACE, "Expected '{' at the beginning of a block")
        
        # Создаем узел блока
        block = ASTNode(ASTNodeType.BLOCK)
        
        # Разбираем операторы
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            block.add_child(stmt)
        
        # Ожидаем закрывающую фигурную скобку
        self._consume(TokenType.RBRACE, "Expected '}' at the end of a block")
        
        return block
    
    def _parse_statement(self) -> ASTNode:
        """
        Разбирает оператор.
        
        Returns:
            Узел оператора
        """
        # Проверяем, какой оператор перед нами
        if self._match(TokenType.IF):
            return self._parse_if_statement()
        elif self._match(TokenType.WHILE):
            return self._parse_while_statement()
        elif self._match(TokenType.FOR):
            return self._parse_for_statement()
        elif self._match(TokenType.FOREACH):
            return self._parse_foreach_statement()
        elif self._match(TokenType.RETURN):
            return self._parse_return_statement()
        elif self._match(TokenType.REQUIRE):
            return self._parse_require_statement()
        elif self._match(TokenType.ASSERT):
            return self._parse_assert_statement()
        elif self._match(TokenType.REVERT):
            return self._parse_revert_statement()
        elif self._match(TokenType.EMIT):
            return self._parse_emit_statement()
        elif self._match(TokenType.TRY):
            return self._parse_try_catch_statement()
        elif self._match(TokenType.LET):
            return self._parse_variable_declaration()
        elif self._check(TokenType.LBRACE):
            return self._parse_block()
        else:
            # Если ничего не подошло, предполагаем, что это выражение
            expr = self._parse_expression()
            
            # Ожидаем точку с запятой
            self._consume(TokenType.SEMICOLON, "Expected ';' after expression statement")
            
            return expr

    # Здесь будут методы для разбора выражений и других операторов
    # (_parse_if_statement, _parse_while_statement, и т.д.)
    
    def _parse_expression(self) -> ASTNode:
        """
        Разбирает выражение (заглушка).
        
        Returns:
            Узел выражения
        """
        # В реальном парсере здесь был бы полноценный разбор выражений
        # Для простоты вернем просто узел идентификатора
        identifier = self._consume(TokenType.IDENTIFIER, "Expected expression")
        return ASTNode(ASTNodeType.IDENTIFIER, name=identifier.value)


# Пример использования
if __name__ == "__main__":
    from lexer import Lexer
    
    # Пример кода на Grishex
    source_code = """
    pragma grishex 1.0;
    
    contract SimpleToken {
        state {
            name: string;
            symbol: string;
            decimals: uint;
        }
        
        constructor(name: string, symbol: string, decimals: uint) {
            self.name = name;
            self.symbol = symbol;
            self.decimals = decimals;
        }
    }
    """
    
    # Создаем лексический анализатор
    lexer = Lexer(source_code)
    
    # Получаем токены
    tokens = lexer.tokenize()
    
    # Создаем синтаксический анализатор
    parser = Parser(tokens)
    
    # Строим AST
    ast = parser.parse()
    
    # Выводим AST для отладки
    print(f"AST: {ast}")
    print(f"Children: {len(ast.children)}")
    
    # Проверяем ошибки
    if parser.errors:
        print("Errors:")
        for error in parser.errors:
            print(f"  {error}")
    else:
        print("No errors!") 