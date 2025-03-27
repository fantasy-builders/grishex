#!/usr/bin/env python3
"""
Grishex - Компилятор

Модуль для преобразования AST в байт-код.
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum, auto
from parser import ASTNode, ASTNodeType


class CompilerError(Exception):
    """Исключение, возникающее при ошибке компиляции."""
    
    def __init__(self, message: str, node: Optional[ASTNode] = None):
        """
        Инициализирует исключение.
        
        Args:
            message: Сообщение об ошибке
            node: Узел AST, вызвавший ошибку
        """
        self.message = message
        self.node = node
        super().__init__(message)


class SymbolType(Enum):
    """Типы символов в таблице символов."""
    CONTRACT = auto()
    INTERFACE = auto()
    FUNCTION = auto()
    VAR = auto()
    PARAM = auto()
    STATE_VAR = auto()
    EVENT = auto()
    STRUCT = auto()
    ENUM = auto()
    ENUM_VALUE = auto()


class Symbol:
    """Символ в таблице символов."""
    
    def __init__(self, name: str, symbol_type: SymbolType, **kwargs):
        """
        Инициализирует символ.
        
        Args:
            name: Имя символа
            symbol_type: Тип символа
            **kwargs: Дополнительные атрибуты символа
        """
        self.name = name
        self.symbol_type = symbol_type
        self.attributes = kwargs
    
    def __repr__(self) -> str:
        """
        Возвращает строковое представление символа.
        
        Returns:
            Строковое представление символа
        """
        return f"Symbol({self.name}, {self.symbol_type})"


class SymbolTable:
    """Таблица символов для хранения информации о переменных, функциях и других сущностях."""
    
    def __init__(self, parent: Optional['SymbolTable'] = None):
        """
        Инициализирует таблицу символов.
        
        Args:
            parent: Родительская таблица символов
        """
        self.symbols = {}
        self.parent = parent
    
    def define(self, name: str, symbol_type: SymbolType, **kwargs) -> Symbol:
        """
        Определяет символ в таблице.
        
        Args:
            name: Имя символа
            symbol_type: Тип символа
            **kwargs: Дополнительные атрибуты символа
            
        Returns:
            Созданный символ
        """
        symbol = Symbol(name, symbol_type, **kwargs)
        self.symbols[name] = symbol
        return symbol
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """
        Ищет символ по имени.
        
        Args:
            name: Имя символа
            
        Returns:
            Найденный символ или None, если символ не найден
        """
        if name in self.symbols:
            return self.symbols[name]
        
        if self.parent:
            return self.parent.resolve(name)
        
        return None
    
    def contains(self, name: str) -> bool:
        """
        Проверяет, содержится ли символ в таблице.
        
        Args:
            name: Имя символа
            
        Returns:
            True, если символ найден, иначе False
        """
        return name in self.symbols


class Compiler:
    """Компилятор для языка Grishex."""
    
    def __init__(self):
        """Инициализирует компилятор."""
        self.reset()
    
    def reset(self):
        """Сбрасывает состояние компилятора."""
        # Байт-код
        self.bytecode = {
            "version": "1.0",
            "contracts": {}
        }
        
        # Глобальная таблица символов
        self.global_symbols = SymbolTable()
        
        # Текущая таблица символов
        self.current_symbols = self.global_symbols
        
        # Счетчики
        self.current_contract = None
        self.current_function = None
        self.current_block = None
        
        # Счетчики для переменных
        self.state_var_count = 0
        self.local_var_count = 0
        self.label_count = 0
        
        # Ошибки
        self.errors = []
    
    def compile(self, ast: ASTNode) -> Dict[str, Any]:
        """
        Компилирует AST в байт-код.
        
        Args:
            ast: Корень AST
            
        Returns:
            Скомпилированный байт-код
        """
        try:
            # Проверяем, что корень AST - программа
            if ast.node_type != ASTNodeType.PROGRAM:
                self.errors.append(CompilerError("Expected program node"))
                return self.bytecode
            
            # Первый проход: сбор информации о контрактах, интерфейсах и структурах
            self._gather_declarations(ast)
            
            # Проверяем ошибки после первого прохода
            if self.errors:
                return self.bytecode
            
            # Второй проход: компиляция контрактов и функций
            self._compile_program(ast)
            
            return self.bytecode
        
        except CompilerError as e:
            self.errors.append(e)
            return self.bytecode
    
    def _gather_declarations(self, program: ASTNode):
        """
        Собирает информацию о контрактах, интерфейсах и структурах.
        
        Args:
            program: Узел программы
        """
        # Обходим все дочерние узлы программы
        for node in program.children:
            if node.node_type == ASTNodeType.CONTRACT:
                # Собираем информацию о контракте
                contract_name = node.get_attribute('name')
                
                # Проверяем, что контракт с таким именем еще не определен
                if self.global_symbols.contains(contract_name):
                    self.errors.append(CompilerError(f"Contract {contract_name} already defined", node))
                    continue
                
                # Определяем контракт в глобальной таблице символов
                self.global_symbols.define(contract_name, SymbolType.CONTRACT, node=node)
                
                # Создаем байт-код для контракта
                self.bytecode["contracts"][contract_name] = {
                    "state_variables": {},
                    "functions": {},
                    "events": {}
                }
            
            elif node.node_type == ASTNodeType.INTERFACE:
                # Собираем информацию об интерфейсе
                interface_name = node.get_attribute('name')
                
                # Проверяем, что интерфейс с таким именем еще не определен
                if self.global_symbols.contains(interface_name):
                    self.errors.append(CompilerError(f"Interface {interface_name} already defined", node))
                    continue
                
                # Определяем интерфейс в глобальной таблице символов
                self.global_symbols.define(interface_name, SymbolType.INTERFACE, node=node)
            
            elif node.node_type == ASTNodeType.STRUCT:
                # Собираем информацию о структуре
                struct_name = node.get_attribute('name')
                
                # Проверяем, что структура с таким именем еще не определена
                if self.global_symbols.contains(struct_name):
                    self.errors.append(CompilerError(f"Struct {struct_name} already defined", node))
                    continue
                
                # Определяем структуру в глобальной таблице символов
                self.global_symbols.define(struct_name, SymbolType.STRUCT, node=node)
            
            elif node.node_type == ASTNodeType.ENUM:
                # Собираем информацию о перечислении
                enum_name = node.get_attribute('name')
                
                # Проверяем, что перечисление с таким именем еще не определено
                if self.global_symbols.contains(enum_name):
                    self.errors.append(CompilerError(f"Enum {enum_name} already defined", node))
                    continue
                
                # Определяем перечисление в глобальной таблице символов
                self.global_symbols.define(enum_name, SymbolType.ENUM, node=node)
                
                # Определяем значения перечисления
                for i, value_node in enumerate(node.children):
                    if value_node.node_type == ASTNodeType.IDENTIFIER:
                        value_name = value_node.get_attribute('name')
                        
                        # Проверяем, что значение с таким именем еще не определено
                        if self.global_symbols.contains(value_name):
                            self.errors.append(CompilerError(f"Enum value {value_name} already defined", value_node))
                            continue
                        
                        # Определяем значение перечисления в глобальной таблице символов
                        self.global_symbols.define(value_name, SymbolType.ENUM_VALUE, enum_name=enum_name, value=i)
    
    def _compile_program(self, program: ASTNode):
        """
        Компилирует программу.
        
        Args:
            program: Узел программы
        """
        # Обходим все дочерние узлы программы
        for node in program.children:
            if node.node_type == ASTNodeType.CONTRACT:
                # Компилируем контракт
                self._compile_contract(node)
            
            # Интерфейсы и другие объявления будут обработаны в будущих версиях
    
    def _compile_contract(self, contract: ASTNode):
        """
        Компилирует контракт.
        
        Args:
            contract: Узел контракта
        """
        # Получаем имя контракта
        contract_name = contract.get_attribute('name')
        
        # Устанавливаем текущий контракт
        self.current_contract = contract_name
        
        # Создаем таблицу символов для контракта
        contract_symbols = SymbolTable(self.global_symbols)
        self.current_symbols = contract_symbols
        
        # Счетчик для переменных состояния
        self.state_var_count = 0
        
        # Обходим все дочерние узлы контракта
        for node in contract.children:
            if node.node_type == ASTNodeType.STATE:
                # Компилируем переменные состояния
                self._compile_state_variables(node)
            elif node.node_type == ASTNodeType.CONSTRUCTOR:
                # Компилируем конструктор
                self._compile_constructor(node)
            elif node.node_type == ASTNodeType.FUNCTION:
                # Компилируем функцию
                self._compile_function(node)
            elif node.node_type == ASTNodeType.EVENT:
                # Компилируем событие
                self._compile_event(node)
        
        # Восстанавливаем текущую таблицу символов
        self.current_symbols = self.global_symbols
        
        # Сбрасываем текущий контракт
        self.current_contract = None

    def _compile_state_variables(self, state: ASTNode):
        """
        Компилирует переменные состояния.
        
        Args:
            state: Узел состояния
        """
        # Обходим все дочерние узлы состояния (переменные)
        for node in state.children:
            if node.node_type == ASTNodeType.VAR_DECLARATION:
                # Получаем имя переменной
                var_name = node.get_attribute('name')
                
                # Проверяем, что переменная с таким именем еще не определена
                if self.current_symbols.contains(var_name):
                    self.errors.append(CompilerError(f"Variable {var_name} already defined", node))
                    continue
                
                # Получаем тип переменной
                type_node = node.children[0]
                type_name = type_node.get_attribute('name')
                
                # Проверяем, что тип существует
                if not self._is_valid_type(type_name):
                    self.errors.append(CompilerError(f"Unknown type {type_name}", type_node))
                    continue
                
                # Определяем переменную в таблице символов
                self.current_symbols.define(var_name, SymbolType.STATE_VAR, 
                                        type=type_name, offset=self.state_var_count)
                
                # Добавляем переменную в байт-код контракта
                self.bytecode["contracts"][self.current_contract]["state_variables"][var_name] = {
                    "type": type_name,
                    "offset": self.state_var_count
                }
                
                # Увеличиваем счетчик переменных состояния
                self.state_var_count += 1
    
    def _compile_constructor(self, constructor: ASTNode):
        """
        Компилирует конструктор.
        
        Args:
            constructor: Узел конструктора
        """
        # Создаем таблицу символов для конструктора
        constructor_symbols = SymbolTable(self.current_symbols)
        self.current_symbols = constructor_symbols
        
        # Устанавливаем текущую функцию
        self.current_function = "constructor"
        
        # Счетчик для локальных переменных
        self.local_var_count = 0
        
        # Код функции
        code = []
        
        # Компилируем параметры
        params = []
        for i, param_node in enumerate(constructor.children[:-1]):
            if param_node.node_type == ASTNodeType.PARAM:
                # Получаем имя параметра
                param_name = param_node.get_attribute('name')
                
                # Проверяем, что параметр с таким именем еще не определен
                if self.current_symbols.contains(param_name):
                    self.errors.append(CompilerError(f"Parameter {param_name} already defined", param_node))
                    continue
                
                # Получаем тип параметра
                type_node = param_node.children[0]
                type_name = type_node.get_attribute('name')
                
                # Проверяем, что тип существует
                if not self._is_valid_type(type_name):
                    self.errors.append(CompilerError(f"Unknown type {type_name}", type_node))
                    continue
                
                # Определяем параметр в таблице символов
                self.current_symbols.define(param_name, SymbolType.PARAM, 
                                         type=type_name, index=i)
                
                # Добавляем параметр в список
                params.append({
                    "name": param_name,
                    "type": type_name
                })
        
        # Компилируем тело конструктора
        body_node = constructor.children[-1]
        body_code = self._compile_block(body_node)
        
        # Добавляем код тела в код функции
        code.extend(body_code)
        
        # Добавляем инструкцию возврата
        code.append({
            "op": "RETURN",
            "value": None
        })
        
        # Добавляем конструктор в байт-код контракта
        self.bytecode["contracts"][self.current_contract]["functions"]["constructor"] = {
            "params": params,
            "code": code
        }
        
        # Восстанавливаем текущую таблицу символов
        self.current_symbols = self.current_symbols.parent
        
        # Сбрасываем текущую функцию
        self.current_function = None
    
    def _compile_function(self, function: ASTNode):
        """
        Компилирует функцию.
        
        Args:
            function: Узел функции
        """
        # Получаем имя функции
        function_name = function.get_attribute('name')
        
        # Проверяем, что функция с таким именем еще не определена
        if self.current_symbols.contains(function_name):
            self.errors.append(CompilerError(f"Function {function_name} already defined", function))
            return
        
        # Создаем таблицу символов для функции
        function_symbols = SymbolTable(self.current_symbols)
        self.current_symbols = function_symbols
        
        # Устанавливаем текущую функцию
        self.current_function = function_name
        
        # Счетчик для локальных переменных
        self.local_var_count = 0
        
        # Код функции
        code = []
        
        # Компилируем параметры
        params = []
        for i, param_node in enumerate(function.children[:-1]):
            if param_node.node_type == ASTNodeType.PARAM:
                # Получаем имя параметра
                param_name = param_node.get_attribute('name')
                
                # Проверяем, что параметр с таким именем еще не определен
                if self.current_symbols.contains(param_name):
                    self.errors.append(CompilerError(f"Parameter {param_name} already defined", param_node))
                    continue
                
                # Получаем тип параметра
                type_node = param_node.children[0]
                type_name = type_node.get_attribute('name')
                
                # Проверяем, что тип существует
                if not self._is_valid_type(type_name):
                    self.errors.append(CompilerError(f"Unknown type {type_name}", type_node))
                    continue
                
                # Определяем параметр в таблице символов
                self.current_symbols.define(param_name, SymbolType.PARAM, 
                                         type=type_name, index=i)
                
                # Добавляем параметр в список
                params.append({
                    "name": param_name,
                    "type": type_name
                })
        
        # Получаем возвращаемый тип
        return_type = None
        if 'return_type' in function.attributes:
            return_type_node = function.get_attribute('return_type')
            return_type = return_type_node.get_attribute('name')
            
            # Проверяем, что тип существует
            if not self._is_valid_type(return_type):
                self.errors.append(CompilerError(f"Unknown return type {return_type}", return_type_node))
                return_type = None
        
        # Компилируем тело функции
        body_node = function.children[-1]
        body_code = self._compile_block(body_node)
        
        # Добавляем код тела в код функции
        code.extend(body_code)
        
        # Если функция должна что-то возвращать, но нет инструкции return
        # добавляем инструкцию возврата со значением по умолчанию
        if return_type and not any(instr.get("op") == "RETURN" for instr in code):
            code.append({
                "op": "RETURN",
                "value": self._default_value_for_type(return_type)
            })
        
        # Добавляем функцию в байт-код контракта
        is_view = function.get_attribute('is_view', False)
        is_private = function.get_attribute('is_private', False)
        
        self.bytecode["contracts"][self.current_contract]["functions"][function_name] = {
            "params": params,
            "return_type": return_type,
            "is_view": is_view,
            "is_private": is_private,
            "code": code
        }
        
        # Определяем функцию в таблице символов
        self.current_symbols.parent.define(function_name, SymbolType.FUNCTION, 
                                      return_type=return_type, 
                                      is_view=is_view, 
                                      is_private=is_private)
        
        # Восстанавливаем текущую таблицу символов
        self.current_symbols = self.current_symbols.parent
        
        # Сбрасываем текущую функцию
        self.current_function = None
    
    def _compile_event(self, event: ASTNode):
        """
        Компилирует событие.
        
        Args:
            event: Узел события
        """
        # Получаем имя события
        event_name = event.get_attribute('name')
        
        # Проверяем, что событие с таким именем еще не определено
        if self.current_symbols.contains(event_name):
            self.errors.append(CompilerError(f"Event {event_name} already defined", event))
            return
        
        # Компилируем параметры
        params = []
        for param_node in event.children:
            if param_node.node_type == ASTNodeType.PARAM:
                # Получаем имя параметра
                param_name = param_node.get_attribute('name')
                
                # Получаем тип параметра
                type_node = param_node.children[0]
                type_name = type_node.get_attribute('name')
                
                # Проверяем, что тип существует
                if not self._is_valid_type(type_name):
                    self.errors.append(CompilerError(f"Unknown type {type_name}", type_node))
                    continue
                
                # Добавляем параметр в список
                params.append({
                    "name": param_name,
                    "type": type_name
                })
        
        # Добавляем событие в байт-код контракта
        self.bytecode["contracts"][self.current_contract]["events"][event_name] = {
            "params": params
        }
        
        # Определяем событие в таблице символов
        self.current_symbols.define(event_name, SymbolType.EVENT, params=params)
    
    def _compile_block(self, block: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует блок кода.
        
        Args:
            block: Узел блока
            
        Returns:
            Скомпилированный код блока
        """
        # Создаем таблицу символов для блока
        block_symbols = SymbolTable(self.current_symbols)
        old_symbols = self.current_symbols
        self.current_symbols = block_symbols
        
        # Код блока
        code = []
        
        # Компилируем операторы
        for stmt_node in block.children:
            stmt_code = self._compile_statement(stmt_node)
            code.extend(stmt_code)
        
        # Восстанавливаем текущую таблицу символов
        self.current_symbols = old_symbols
        
        return code
    
    def _compile_statement(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует оператор.
        
        Args:
            stmt: Узел оператора
            
        Returns:
            Скомпилированный код оператора
        """
        # В зависимости от типа оператора вызываем соответствующий метод
        if stmt.node_type == ASTNodeType.BLOCK:
            return self._compile_block(stmt)
        elif stmt.node_type == ASTNodeType.VAR_DECLARATION:
            return self._compile_var_declaration(stmt)
        elif stmt.node_type == ASTNodeType.ASSIGNMENT:
            return self._compile_assignment(stmt)
        elif stmt.node_type == ASTNodeType.IF_STMT:
            return self._compile_if_statement(stmt)
        elif stmt.node_type == ASTNodeType.WHILE_STMT:
            return self._compile_while_statement(stmt)
        elif stmt.node_type == ASTNodeType.FOR_STMT:
            return self._compile_for_statement(stmt)
        elif stmt.node_type == ASTNodeType.FOREACH_STMT:
            return self._compile_foreach_statement(stmt)
        elif stmt.node_type == ASTNodeType.RETURN_STMT:
            return self._compile_return_statement(stmt)
        elif stmt.node_type == ASTNodeType.REQUIRE_STMT:
            return self._compile_require_statement(stmt)
        elif stmt.node_type == ASTNodeType.ASSERT_STMT:
            return self._compile_assert_statement(stmt)
        elif stmt.node_type == ASTNodeType.REVERT_STMT:
            return self._compile_revert_statement(stmt)
        elif stmt.node_type == ASTNodeType.EMIT_STMT:
            return self._compile_emit_statement(stmt)
        elif stmt.node_type == ASTNodeType.TRY_CATCH_STMT:
            return self._compile_try_catch_statement(stmt)
        elif stmt.node_type in [ASTNodeType.BINARY_EXPR, ASTNodeType.UNARY_EXPR, 
                               ASTNodeType.LITERAL, ASTNodeType.IDENTIFIER, 
                               ASTNodeType.MEMBER_ACCESS, ASTNodeType.INDEX_ACCESS, 
                               ASTNodeType.CALL_EXPR]:
            # Выражение
            code = self._compile_expression(stmt)
            
            # Удаляем результат выражения со стека, если он не нужен
            code.append({
                "op": "POP"
            })
            
            return code
        else:
            # Неизвестный тип оператора
            self.errors.append(CompilerError(f"Unknown statement type: {stmt.node_type}", stmt))
            return []
    
    def _is_valid_type(self, type_name: str) -> bool:
        """
        Проверяет, является ли тип допустимым.
        
        Args:
            type_name: Имя типа
            
        Returns:
            True, если тип допустим, иначе False
        """
        # Примитивные типы
        primitive_types = [
            "int", "uint", "bool", "address", "string", "bytes", "hash", "float"
        ]
        
        if type_name in primitive_types:
            return True
        
        # Массивы и отображения - тип.startswith() - в реальной реализации
        # нужна более сложная проверка
        
        # Пользовательские типы (структуры и перечисления)
        symbol = self.global_symbols.resolve(type_name)
        if symbol and symbol.symbol_type in [SymbolType.STRUCT, SymbolType.ENUM]:
            return True
        
        return False
    
    def _default_value_for_type(self, type_name: str) -> Any:
        """
        Возвращает значение по умолчанию для типа.
        
        Args:
            type_name: Имя типа
            
        Returns:
            Значение по умолчанию
        """
        if type_name in ["int", "uint"]:
            return 0
        elif type_name == "bool":
            return False
        elif type_name == "float":
            return 0.0
        elif type_name == "address":
            return "0x0000000000000000000000000000000000000000"
        elif type_name == "string":
            return ""
        elif type_name == "bytes":
            return b""
        elif type_name == "hash":
            return "0x0000000000000000000000000000000000000000000000000000000000000000"
        else:
            # Для пользовательских типов
            return None
    
    def _compile_expression(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует выражение.
        
        Args:
            expr: Узел выражения
            
        Returns:
            Скомпилированный код выражения
        """
        # В зависимости от типа выражения вызываем соответствующий метод
        if expr.node_type == ASTNodeType.BINARY_EXPR:
            return self._compile_binary_expression(expr)
        elif expr.node_type == ASTNodeType.UNARY_EXPR:
            return self._compile_unary_expression(expr)
        elif expr.node_type == ASTNodeType.LITERAL:
            return self._compile_literal(expr)
        elif expr.node_type == ASTNodeType.IDENTIFIER:
            return self._compile_identifier(expr)
        elif expr.node_type == ASTNodeType.MEMBER_ACCESS:
            return self._compile_member_access(expr)
        elif expr.node_type == ASTNodeType.INDEX_ACCESS:
            return self._compile_index_access(expr)
        elif expr.node_type == ASTNodeType.CALL_EXPR:
            return self._compile_call_expression(expr)
        else:
            # Неизвестный тип выражения
            self.errors.append(CompilerError(f"Unknown expression type: {expr.node_type}", expr))
            return []
    
    def _compile_binary_expression(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует бинарное выражение.
        
        Args:
            expr: Узел бинарного выражения
            
        Returns:
            Скомпилированный код бинарного выражения
        """
        # Получаем оператор
        operator = expr.get_attribute('operator')
        
        # Получаем левое и правое выражения
        left = expr.children[0]
        right = expr.children[1]
        
        # Код бинарного выражения
        code = []
        
        # Компилируем левое и правое выражения
        left_code = self._compile_expression(left)
        right_code = self._compile_expression(right)
        
        # Добавляем код левого и правого выражений
        code.extend(left_code)
        code.extend(right_code)
        
        # Добавляем инструкцию в зависимости от оператора
        if operator == '+':
            code.append({"op": "ADD"})
        elif operator == '-':
            code.append({"op": "SUB"})
        elif operator == '*':
            code.append({"op": "MUL"})
        elif operator == '/':
            code.append({"op": "DIV"})
        elif operator == '%':
            code.append({"op": "MOD"})
        elif operator == '==':
            code.append({"op": "EQ"})
        elif operator == '!=':
            code.append({"op": "NEQ"})
        elif operator == '<':
            code.append({"op": "LT"})
        elif operator == '>':
            code.append({"op": "GT"})
        elif operator == '<=':
            code.append({"op": "LTE"})
        elif operator == '>=':
            code.append({"op": "GTE"})
        elif operator == '&&':
            code.append({"op": "AND"})
        elif operator == '||':
            code.append({"op": "OR"})
        else:
            # Неизвестный оператор
            self.errors.append(CompilerError(f"Unknown binary operator: {operator}", expr))
        
        return code
    
    def _compile_unary_expression(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует унарное выражение.
        
        Args:
            expr: Узел унарного выражения
            
        Returns:
            Скомпилированный код унарного выражения
        """
        # Получаем оператор
        operator = expr.get_attribute('operator')
        
        # Получаем выражение
        expression = expr.children[0]
        
        # Код унарного выражения
        code = []
        
        # Компилируем выражение
        expr_code = self._compile_expression(expression)
        code.extend(expr_code)
        
        # Добавляем инструкцию в зависимости от оператора
        if operator == '-':
            code.append({"op": "NEG"})
        elif operator == '!':
            code.append({"op": "NOT"})
        else:
            # Неизвестный оператор
            self.errors.append(CompilerError(f"Unknown unary operator: {operator}", expr))
        
        return code
    
    def _compile_literal(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует литерал.
        
        Args:
            expr: Узел литерала
            
        Returns:
            Скомпилированный код литерала
        """
        # Получаем тип и значение литерала
        literal_type = expr.get_attribute('type')
        value = expr.get_attribute('value')
        
        # Код литерала
        code = []
        
        # Добавляем инструкцию PUSH
        code.append({
            "op": "PUSH",
            "value": value
        })
        
        return code
    
    def _compile_identifier(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует идентификатор.
        
        Args:
            expr: Узел идентификатора
            
        Returns:
            Скомпилированный код идентификатора
        """
        # Получаем имя идентификатора
        name = expr.get_attribute('name')
        
        # Ищем символ в таблице символов
        symbol = self.current_symbols.resolve(name)
        
        # Код идентификатора
        code = []
        
        if symbol:
            if symbol.symbol_type == SymbolType.VAR:
                # Локальная переменная
                code.append({
                    "op": "LOAD_LOCAL",
                    "index": symbol.attributes["index"]
                })
            elif symbol.symbol_type == SymbolType.PARAM:
                # Параметр функции
                code.append({
                    "op": "LOAD_LOCAL",
                    "index": symbol.attributes["index"]
                })
            elif symbol.symbol_type == SymbolType.STATE_VAR:
                # Переменная состояния
                code.append({
                    "op": "LOAD_STATE",
                    "offset": symbol.attributes["offset"]
                })
            elif symbol.symbol_type == SymbolType.ENUM_VALUE:
                # Значение перечисления
                code.append({
                    "op": "PUSH",
                    "value": symbol.attributes["value"]
                })
            elif name == "self":
                # Ключевое слово self
                code.append({
                    "op": "PUSH",
                    "value": "self"
                })
            else:
                # Другие типы символов
                self.errors.append(CompilerError(f"Cannot use {name} as an expression", expr))
        else:
            # Символ не найден
            self.errors.append(CompilerError(f"Undefined identifier: {name}", expr))
        
        return code
    
    def _compile_member_access(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует доступ к члену объекта.
        
        Args:
            expr: Узел доступа к члену
            
        Returns:
            Скомпилированный код доступа к члену
        """
        # Получаем объект и имя члена
        obj = expr.children[0]
        member = expr.get_attribute('member')
        
        # Код доступа к члену
        code = []
        
        # Компилируем объект
        obj_code = self._compile_expression(obj)
        code.extend(obj_code)
        
        # Добавляем инструкцию LOAD_MEMBER
        code.append({
            "op": "LOAD_MEMBER",
            "member": member
        })
        
        return code
    
    def _compile_index_access(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует доступ по индексу.
        
        Args:
            expr: Узел доступа по индексу
            
        Returns:
            Скомпилированный код доступа по индексу
        """
        # Получаем объект и индекс
        obj = expr.children[0]
        index = expr.children[1]
        
        # Код доступа по индексу
        code = []
        
        # Компилируем объект и индекс
        obj_code = self._compile_expression(obj)
        index_code = self._compile_expression(index)
        
        code.extend(obj_code)
        code.extend(index_code)
        
        # Добавляем инструкцию LOAD_INDEX
        code.append({
            "op": "LOAD_INDEX"
        })
        
        return code
    
    def _compile_call_expression(self, expr: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует вызов функции.
        
        Args:
            expr: Узел вызова функции
            
        Returns:
            Скомпилированный код вызова функции
        """
        # Получаем функцию и аргументы
        func = expr.get_attribute('function')
        args = expr.children
        
        # Код вызова функции
        code = []
        
        # Компилируем аргументы
        for arg in args:
            arg_code = self._compile_expression(arg)
            code.extend(arg_code)
        
        # Добавляем инструкцию CALL
        code.append({
            "op": "CALL",
            "function": func,
            "args_count": len(args)
        })
        
        return code
    
    def _compile_var_declaration(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует объявление переменной.
        
        Args:
            stmt: Узел объявления переменной
            
        Returns:
            Скомпилированный код объявления переменной
        """
        # Получаем имя переменной
        var_name = stmt.get_attribute('name')
        
        # Проверяем, что переменная с таким именем еще не определена
        if self.current_symbols.contains(var_name):
            self.errors.append(CompilerError(f"Variable {var_name} already defined", stmt))
            return []
        
        # Получаем тип переменной
        type_node = stmt.children[0]
        type_name = type_node.get_attribute('name')
        
        # Проверяем, что тип существует
        if not self._is_valid_type(type_name):
            self.errors.append(CompilerError(f"Unknown type {type_name}", type_node))
            return []
        
        # Код объявления переменной
        code = []
        
        # Если есть инициализатор, компилируем его
        if len(stmt.children) > 1:
            initializer = stmt.children[1]
            
            # Компилируем инициализатор
            init_code = self._compile_expression(initializer)
            code.extend(init_code)
        else:
            # Иначе используем значение по умолчанию
            code.append({
                "op": "PUSH",
                "value": self._default_value_for_type(type_name)
            })
        
        # Определяем переменную в таблице символов
        self.current_symbols.define(var_name, SymbolType.VAR, 
                                type=type_name, index=self.local_var_count)
        
        # Добавляем инструкцию STORE_LOCAL
        code.append({
            "op": "STORE_LOCAL",
            "index": self.local_var_count
        })
        
        # Увеличиваем счетчик локальных переменных
        self.local_var_count += 1
        
        return code
    
    def _compile_assignment(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует присваивание.
        
        Args:
            stmt: Узел присваивания
            
        Returns:
            Скомпилированный код присваивания
        """
        # Получаем левую и правую части
        left = stmt.children[0]
        right = stmt.children[1]
        
        # Код присваивания
        code = []
        
        # Компилируем правую часть
        right_code = self._compile_expression(right)
        code.extend(right_code)
        
        # Компилируем левую часть в зависимости от ее типа
        if left.node_type == ASTNodeType.IDENTIFIER:
            # Идентификатор
            name = left.get_attribute('name')
            
            # Ищем символ в таблице символов
            symbol = self.current_symbols.resolve(name)
            
            if symbol:
                if symbol.symbol_type == SymbolType.VAR:
                    # Локальная переменная
                    code.append({
                        "op": "STORE_LOCAL",
                        "index": symbol.attributes["index"]
                    })
                elif symbol.symbol_type == SymbolType.PARAM:
                    # Параметр функции
                    code.append({
                        "op": "STORE_LOCAL",
                        "index": symbol.attributes["index"]
                    })
                elif symbol.symbol_type == SymbolType.STATE_VAR:
                    # Переменная состояния
                    code.append({
                        "op": "STORE_STATE",
                        "offset": symbol.attributes["offset"]
                    })
                else:
                    # Другие типы символов
                    self.errors.append(CompilerError(f"Cannot assign to {name}", left))
            else:
                # Символ не найден
                self.errors.append(CompilerError(f"Undefined identifier: {name}", left))
        
        elif left.node_type == ASTNodeType.MEMBER_ACCESS:
            # Доступ к члену объекта
            obj = left.children[0]
            member = left.get_attribute('member')
            
            # Компилируем объект
            obj_code = self._compile_expression(obj)
            
            # Дублируем значение правой части
            code.append({
                "op": "DUP"  # Дублируем значение на стеке
            })
            
            # Добавляем код объекта
            code.extend(obj_code)
            
            # Добавляем инструкцию STORE_MEMBER
            code.append({
                "op": "STORE_MEMBER",
                "member": member
            })
        
        elif left.node_type == ASTNodeType.INDEX_ACCESS:
            # Доступ по индексу
            obj = left.children[0]
            index = left.children[1]
            
            # Компилируем объект и индекс
            obj_code = self._compile_expression(obj)
            index_code = self._compile_expression(index)
            
            # Дублируем значение правой части
            code.append({
                "op": "DUP"  # Дублируем значение на стеке
            })
            
            # Добавляем код объекта и индекса
            code.extend(obj_code)
            code.extend(index_code)
            
            # Добавляем инструкцию STORE_INDEX
            code.append({
                "op": "STORE_INDEX"
            })
        
        else:
            # Неизвестный тип левой части
            self.errors.append(CompilerError(f"Invalid assignment target", left))
        
        return code
    
    def _compile_return_statement(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует оператор return.
        
        Args:
            stmt: Узел оператора return
            
        Returns:
            Скомпилированный код оператора return
        """
        # Код оператора return
        code = []
        
        # Если есть выражение, компилируем его
        if stmt.children:
            expr = stmt.children[0]
            
            # Компилируем выражение
            expr_code = self._compile_expression(expr)
            code.extend(expr_code)
            
            # Добавляем инструкцию RETURN
            code.append({
                "op": "RETURN",
                "value": "stack"
            })
        else:
            # Иначе возвращаем None
            code.append({
                "op": "RETURN",
                "value": None
            })
        
        return code
    
    def _compile_if_statement(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует условный оператор.
        
        Args:
            stmt: Узел условного оператора
            
        Returns:
            Скомпилированный код условного оператора
        """
        # Получаем условие, блок if и блок else (если есть)
        condition = stmt.children[0]
        if_block = stmt.children[1]
        else_block = stmt.children[2] if len(stmt.children) > 2 else None
        
        # Код условного оператора
        code = []
        
        # Компилируем условие
        condition_code = self._compile_expression(condition)
        code.extend(condition_code)
        
        # Если нет блока else
        if not else_block:
            # Генерируем метку
            end_if_label = self.label_count
            self.label_count += 1
            
            # Добавляем инструкцию JUMP_IF_FALSE
            code.append({
                "op": "JUMP_IF_FALSE",
                "offset": 0  # Будет заполнено позже
            })
            
            # Запоминаем индекс инструкции JUMP_IF_FALSE
            jump_if_false_index = len(code) - 1
            
            # Компилируем блок if
            if_code = self._compile_statement(if_block)
            code.extend(if_code)
            
            # Заполняем смещение для JUMP_IF_FALSE
            code[jump_if_false_index]["offset"] = len(if_code) + 1
        else:
            # Генерируем метки
            else_label = self.label_count
            self.label_count += 1
            end_if_label = self.label_count
            self.label_count += 1
            
            # Добавляем инструкцию JUMP_IF_FALSE
            code.append({
                "op": "JUMP_IF_FALSE",
                "offset": 0  # Будет заполнено позже
            })
            
            # Запоминаем индекс инструкции JUMP_IF_FALSE
            jump_if_false_index = len(code) - 1
            
            # Компилируем блок if
            if_code = self._compile_statement(if_block)
            code.extend(if_code)
            
            # Добавляем инструкцию JUMP
            code.append({
                "op": "JUMP",
                "offset": 0  # Будет заполнено позже
            })
            
            # Запоминаем индекс инструкции JUMP
            jump_index = len(code) - 1
            
            # Заполняем смещение для JUMP_IF_FALSE
            code[jump_if_false_index]["offset"] = len(if_code) + 1
            
            # Компилируем блок else
            else_code = self._compile_statement(else_block)
            code.extend(else_code)
            
            # Заполняем смещение для JUMP
            code[jump_index]["offset"] = len(else_code) + 1
        
        return code
    
    def _compile_require_statement(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует оператор require.
        
        Args:
            stmt: Узел оператора require
            
        Returns:
            Скомпилированный код оператора require
        """
        # Получаем условие и сообщение
        condition = stmt.children[0]
        message = stmt.get_attribute('message', 'Requirement failed')
        
        # Код оператора require
        code = []
        
        # Компилируем условие
        condition_code = self._compile_expression(condition)
        code.extend(condition_code)
        
        # Добавляем инструкцию REQUIRE
        code.append({
            "op": "REQUIRE",
            "message": message
        })
        
        return code
    
    def _compile_emit_statement(self, stmt: ASTNode) -> List[Dict[str, Any]]:
        """
        Компилирует оператор emit.
        
        Args:
            stmt: Узел оператора emit
            
        Returns:
            Скомпилированный код оператора emit
        """
        # Получаем событие и аргументы
        event_name = stmt.get_attribute('event')
        args = stmt.children
        
        # Проверяем, что событие определено
        event_symbol = self.current_symbols.resolve(event_name)
        if not event_symbol or event_symbol.symbol_type != SymbolType.EVENT:
            self.errors.append(CompilerError(f"Undefined event: {event_name}", stmt))
            return []
        
        # Проверяем количество аргументов
        event_params = event_symbol.attributes["params"]
        if len(args) != len(event_params):
            self.errors.append(CompilerError(f"Event {event_name} expects {len(event_params)} arguments, got {len(args)}", stmt))
            return []
        
        # Код оператора emit
        code = []
        
        # Компилируем аргументы
        for arg in args:
            arg_code = self._compile_expression(arg)
            code.extend(arg_code)
        
        # Добавляем инструкцию EMIT
        code.append({
            "op": "EMIT",
            "event": event_name,
            "args_count": len(args)
        })
        
        return code


# Пример использования
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    import json
    
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
        
        function getName() view returns string {
            return self.name;
        }
        
        function getSymbol() view returns string {
            return self.symbol;
        }
        
        function getDecimals() view returns uint {
            return self.decimals;
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
    
    # Создаем компилятор
    compiler = Compiler()
    
    # Компилируем AST
    bytecode = compiler.compile(ast)
    
    # Выводим байт-код
    print(json.dumps(bytecode, indent=2))
    
    # Проверяем ошибки
    if compiler.errors:
        print("Errors:")
        for error in compiler.errors:
            print(f"  {error}") 