#!/usr/bin/env python3
"""
Виртуальная машина для языка Grishex.

Выполняет байт-код, сгенерированный компилятором Grishex.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import random
import time


class VMError(Exception):
    """Исключение, возникающее при ошибке выполнения виртуальной машины."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class GrishexVM:
    """Виртуальная машина для выполнения байт-кода Grishex."""
    
    def __init__(self):
        """Инициализирует виртуальную машину."""
        self.reset()
    
    def reset(self):
        """Сбрасывает состояние виртуальной машины."""
        # Контракты
        self.contracts = {}
        
        # Экземпляры контрактов (развернутые контракты с адресами)
        self.contract_instances = {}
        
        # Хранилища контрактов
        self.storage = {}
        
        # Журнал событий
        self.logs = []
        
        # Адреса
        self.addresses = {}
        
        # Стек вызовов
        self.call_stack = []
        
        # Статистика
        self.stats = {
            "gas_used": 0,
            "instructions_executed": 0,
            "function_calls": 0,
            "storage_reads": 0,
            "storage_writes": 0
        }
    
    def load_contract(self, bytecode: Dict[str, Any]) -> None:
        """
        Загружает байт-код контракта в виртуальную машину.
        
        Args:
            bytecode: Байт-код контракта
        """
        # Загружаем контракты
        for contract_name, contract_data in bytecode.get("contracts", {}).items():
            self.contracts[contract_name] = contract_data
    
    def deploy_contract(self, contract_name: str, constructor_args: List[Any] = None) -> str:
        """
        Развертывает контракт.
        
        Args:
            contract_name: Имя контракта
            constructor_args: Аргументы конструктора
            
        Returns:
            Адрес развернутого контракта
        """
        # Проверяем, существует ли контракт
        if contract_name not in self.contracts:
            raise VMError(f"Contract {contract_name} not found")
        
        # Генерируем адрес
        address = f"0x{random.randint(0, 2**160-1):040x}"
        
        # Создаем экземпляр контракта
        self.contract_instances[address] = {
            "name": contract_name,
            "storage_address": address
        }
        
        # Создаем хранилище для контракта
        self.storage[address] = {}
        
        # Сохраняем адрес
        self.addresses[contract_name] = address
        
        # Вызываем конструктор, если он есть
        constructor_args = constructor_args or []
        contract_data = self.contracts[contract_name]
        
        if "constructor" in contract_data.get("functions", {}):
            self.execute_function(contract_name, "constructor", constructor_args, address)
        
        return address
    
    def execute_function(self, contract_name: str, function_name: str, 
                         args: List[Any] = None, contract_address: str = None) -> Any:
        """
        Выполняет функцию контракта.
        
        Args:
            contract_name: Имя контракта
            function_name: Имя функции
            args: Аргументы функции
            contract_address: Адрес контракта (если не указан, используется первый развернутый экземпляр)
            
        Returns:
            Результат выполнения функции
        """
        # Проверяем, существует ли контракт
        if contract_name not in self.contracts:
            raise VMError(f"Contract {contract_name} not found")
        
        # Проверяем, существует ли функция
        contract_data = self.contracts[contract_name]
        if function_name not in contract_data.get("functions", {}):
            raise VMError(f"Function {function_name} not found in contract {contract_name}")
        
        # Получаем адрес контракта
        if not contract_address:
            if contract_name in self.addresses:
                contract_address = self.addresses[contract_name]
            else:
                # Ищем первый развернутый экземпляр контракта
                for address, instance in self.contract_instances.items():
                    if instance["name"] == contract_name:
                        contract_address = address
                        break
                
                if not contract_address:
                    # Если нет развернутых экземпляров, разворачиваем контракт
                    contract_address = self.deploy_contract(contract_name)
        
        # Получаем функцию
        function_data = contract_data["functions"][function_name]
        
        # Проверяем аргументы
        args = args or []
        params = function_data.get("params", [])
        
        if len(args) != len(params):
            raise VMError(f"Expected {len(params)} arguments, got {len(args)}")
        
        # Преобразуем аргументы к нужным типам
        processed_args = []
        for i, arg in enumerate(args):
            param = params[i]
            param_type = param["type"]
            
            # В реальной ВМ здесь был бы код для преобразования типов
            processed_args.append(arg)
        
        # Создаем новый стековый фрейм
        frame = {
            "contract_name": contract_name,
            "contract_address": contract_address,
            "function_name": function_name,
            "locals": {},
            "stack": []
        }
        
        # Добавляем аргументы в локальные переменные
        for i, arg in enumerate(processed_args):
            param = params[i]
            frame["locals"][i] = arg
        
        # Добавляем фрейм в стек вызовов
        self.call_stack.append(frame)
        
        # Обновляем статистику
        self.stats["function_calls"] += 1
        
        # Выполняем код функции
        result = self._execute_code(function_data["code"])
        
        # Удаляем фрейм из стека вызовов
        self.call_stack.pop()
        
        return result
    
    def _execute_code(self, code: List[Dict[str, Any]]) -> Any:
        """
        Выполняет код функции.
        
        Args:
            code: Код функции
            
        Returns:
            Результат выполнения функции
        """
        # Получаем текущий фрейм
        frame = self.call_stack[-1]
        
        # Выполняем инструкции
        i = 0
        while i < len(code):
            instruction = code[i]
            op = instruction["op"]
            
            # Обновляем статистику
            self.stats["instructions_executed"] += 1
            self.stats["gas_used"] += 1  # Упрощенная модель газа
            
            if op == "PUSH":
                # Кладем значение на стек
                value = instruction["value"]
                frame["stack"].append(value)
            
            elif op == "POP":
                # Удаляем значение с вершины стека
                frame["stack"].pop()
            
            elif op == "STORE_LOCAL":
                # Сохраняем значение в локальной переменной
                index = instruction["index"]
                value = frame["stack"].pop()
                frame["locals"][index] = value
            
            elif op == "LOAD_LOCAL":
                # Загружаем значение из локальной переменной
                index = instruction["index"]
                if index in frame["locals"]:
                    value = frame["locals"][index]
                    frame["stack"].append(value)
                else:
                    raise VMError(f"Local variable at index {index} not found")
            
            elif op == "STORE_STATE":
                # Сохраняем значение в хранилище
                offset = instruction["offset"]
                value = frame["stack"].pop()
                
                # Получаем хранилище контракта
                storage = self.storage.get(frame["contract_address"], {})
                storage[offset] = value
                self.storage[frame["contract_address"]] = storage
                
                # Обновляем статистику
                self.stats["storage_writes"] += 1
            
            elif op == "LOAD_STATE":
                # Загружаем значение из хранилища
                offset = instruction["offset"]
                
                # Получаем хранилище контракта
                storage = self.storage.get(frame["contract_address"], {})
                
                # Если переменной нет в хранилище, используем значение по умолчанию
                if offset in storage:
                    value = storage[offset]
                else:
                    value = None
                
                frame["stack"].append(value)
                
                # Обновляем статистику
                self.stats["storage_reads"] += 1
            
            elif op == "STORE_MEMBER":
                # Сохраняем значение в члене объекта
                member = instruction["member"]
                value = frame["stack"].pop()
                obj = frame["stack"].pop()
                
                # Если объект - словарь, сохраняем значение
                if isinstance(obj, dict):
                    obj[member] = value
                else:
                    raise VMError(f"Cannot store member {member} in non-object value")
            
            elif op == "LOAD_MEMBER":
                # Загружаем значение из члена объекта
                member = instruction["member"]
                obj = frame["stack"].pop()
                
                # Если объект - словарь, загружаем значение
                if isinstance(obj, dict):
                    if member in obj:
                        value = obj[member]
                    else:
                        value = None
                    frame["stack"].append(value)
                elif obj == "self":
                    # Если объект - self, загружаем из хранилища
                    storage = self.storage.get(frame["contract_address"], {})
                    contract_data = self.contracts[frame["contract_name"]]
                    
                    if "state_variables" in contract_data and member in contract_data["state_variables"]:
                        var_data = contract_data["state_variables"][member]
                        offset = var_data["offset"]
                        
                        if offset in storage:
                            value = storage[offset]
                        else:
                            value = None
                        
                        frame["stack"].append(value)
                        
                        # Обновляем статистику
                        self.stats["storage_reads"] += 1
                    else:
                        raise VMError(f"State variable {member} not found")
                else:
                    raise VMError(f"Cannot load member {member} from non-object value")
            
            elif op == "LOAD_INDEX":
                # Загружаем значение по индексу
                index = frame["stack"].pop()
                obj = frame["stack"].pop()
                
                # Если объект - список или словарь, загружаем значение
                if isinstance(obj, list) and isinstance(index, int) and 0 <= index < len(obj):
                    value = obj[index]
                    frame["stack"].append(value)
                elif isinstance(obj, dict) and index in obj:
                    value = obj[index]
                    frame["stack"].append(value)
                else:
                    raise VMError(f"Cannot load index {index} from object")
            
            elif op == "CALL":
                # Вызываем функцию
                function_name = instruction["function"]
                args_count = instruction["args_count"]
                
                # Получаем аргументы из стека
                args = []
                for _ in range(args_count):
                    args.insert(0, frame["stack"].pop())
                
                # Вызываем функцию
                if function_name == "print":
                    # Встроенная функция print
                    print(*args)
                    frame["stack"].append(None)
                else:
                    # Ищем функцию в текущем контракте
                    contract_name = frame["contract_name"]
                    contract_data = self.contracts[contract_name]
                    
                    if "functions" in contract_data and function_name in contract_data["functions"]:
                        # Вызываем функцию контракта
                        result = self.execute_function(contract_name, function_name, args, frame["contract_address"])
                        frame["stack"].append(result)
                    else:
                        raise VMError(f"Function {function_name} not found")
            
            elif op == "RETURN":
                # Возвращаем значение
                value = instruction.get("value")
                
                if value == "stack":
                    # Если значение на стеке, возвращаем его
                    if frame["stack"]:
                        return frame["stack"][-1]
                    else:
                        return None
                else:
                    # Иначе возвращаем указанное значение
                    return value
            
            elif op == "JUMP":
                # Безусловный переход
                offset = instruction["offset"]
                i += offset
                continue
            
            elif op == "JUMP_IF_FALSE":
                # Условный переход
                offset = instruction["offset"]
                condition = frame["stack"].pop()
                
                if not condition:
                    i += offset
                    continue
            
            elif op == "REQUIRE":
                # Проверка условия
                condition = frame["stack"].pop()
                message = instruction.get("message", "Requirement failed")
                
                if not condition:
                    raise VMError(message)
            
            elif op == "EMIT":
                # Генерация события
                event_name = instruction["event"]
                args_count = instruction["args_count"]
                
                # Получаем аргументы из стека
                args = []
                for _ in range(args_count):
                    args.insert(0, frame["stack"].pop())
                
                # Получаем контракт и адрес
                contract_name = frame["contract_name"]
                contract_address = frame["contract_address"]
                
                # Создаем запись в журнале
                log = {
                    "contract": contract_name,
                    "address": contract_address,
                    "event": event_name,
                    "topics": [],
                    "data": args
                }
                
                # Добавляем запись в журнал
                self.logs.append(log)
            
            elif op == "ADD":
                # Сложение
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a + b)
            
            elif op == "SUB":
                # Вычитание
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a - b)
            
            elif op == "MUL":
                # Умножение
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a * b)
            
            elif op == "DIV":
                # Деление
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                if b == 0:
                    raise VMError("Division by zero")
                frame["stack"].append(a / b)
            
            elif op == "EQ":
                # Равенство
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a == b)
            
            elif op == "NEQ":
                # Неравенство
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a != b)
            
            elif op == "LT":
                # Меньше
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a < b)
            
            elif op == "GT":
                # Больше
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a > b)
            
            elif op == "LTE":
                # Меньше или равно
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a <= b)
            
            elif op == "GTE":
                # Больше или равно
                b = frame["stack"].pop()
                a = frame["stack"].pop()
                frame["stack"].append(a >= b)
            
            elif op == "NEG":
                # Отрицание
                a = frame["stack"].pop()
                frame["stack"].append(-a)
            
            elif op == "NOT":
                # Логическое отрицание
                a = frame["stack"].pop()
                frame["stack"].append(not a)
            
            else:
                raise VMError(f"Unknown opcode: {op}")
            
            i += 1
        
        # Если дошли до конца, возвращаем значение с вершины стека
        if frame["stack"]:
            return frame["stack"][-1]
        else:
            return None
    
    def get_storage(self, contract_name: str = None, contract_address: str = None) -> Dict[int, Any]:
        """
        Возвращает хранилище контракта.
        
        Args:
            contract_name: Имя контракта
            contract_address: Адрес контракта
            
        Returns:
            Хранилище контракта
        """
        # Если указан адрес контракта, используем его
        if contract_address:
            return self.storage.get(contract_address, {})
        
        # Если указано имя контракта, ищем адрес
        if contract_name:
            if contract_name in self.addresses:
                contract_address = self.addresses[contract_name]
                return self.storage.get(contract_address, {})
            
            # Ищем первый развернутый экземпляр контракта
            for address, instance in self.contract_instances.items():
                if instance["name"] == contract_name:
                    return self.storage.get(address, {})
        
        # Если ничего не указано, возвращаем все хранилища
        return self.storage
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """
        Возвращает журнал событий.
        
        Returns:
            Журнал событий
        """
        return self.logs
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику выполнения.
        
        Returns:
            Статистика выполнения
        """
        return self.stats


# Пример использования
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    from compiler import Compiler
    
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
    
    # Создаем виртуальную машину
    vm = GrishexVM()
    
    # Загружаем байт-код
    vm.load_contract(bytecode)
    
    # Развертываем контракт
    address = vm.deploy_contract("SimpleToken", ["Grishinium Token", "GRISH", 18])
    print(f"Contract deployed at: {address}")
    
    # Вызываем функции
    name = vm.execute_function("SimpleToken", "getName")
    symbol = vm.execute_function("SimpleToken", "getSymbol")
    decimals = vm.execute_function("SimpleToken", "getDecimals")
    
    print(f"Name: {name}")
    print(f"Symbol: {symbol}")
    print(f"Decimals: {decimals}")
    
    # Выводим хранилище
    storage = vm.get_storage("SimpleToken")
    print("Storage:")
    for key, value in storage.items():
        print(f"  {key}: {value}")
    
    # Выводим статистику
    stats = vm.get_stats()
    print("Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}") 