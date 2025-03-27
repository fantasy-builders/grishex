# Спецификация языка Grishex

## Обзор

Grishex - это специализированный язык смарт-контрактов для блокчейна Grishinium. Он сочетает в себе простоту синтаксиса, близкого к Python, с сильной типизацией и встроенными механизмами безопасности, специфичными для блокчейна.

## Основные характеристики

- **Сильная статическая типизация**: все переменные и функции имеют явно указанные типы
- **Детерминистическое выполнение**: гарантирует одинаковый результат на всех узлах сети
- **Встроенная защита от переполнения**: автоматическая проверка арифметических операций
- **Ограниченный расход вычислительных ресурсов**: предотвращает DoS-атаки
- **Защита от рекурсии**: ограничение глубины стека вызовов
- **Полная изоляция контрактов**: безопасное взаимодействие между контрактами

## Типы данных

### Примитивные типы

| Тип | Описание | Пример |
|-----|----------|--------|
| `int` | 256-битное целое число со знаком | `let x: int = 42;` |
| `uint` | 256-битное беззнаковое целое число | `let balance: uint = 1000;` |
| `bool` | Логический тип (true/false) | `let is_active: bool = true;` |
| `address` | Адрес в блокчейне Grishinium | `let owner: address = "GRS_1a2b3c...";` |
| `string` | Строка UTF-8 | `let name: string = "Token";` |
| `bytes` | Массив байтов | `let data: bytes = 0x1a2b3c;` |
| `hash` | Хеш (SHA3-256) | `let block_hash: hash = #1a2b3c...;` |

### Составные типы

| Тип | Описание | Пример |
|-----|----------|--------|
| `array<T>` | Массив элементов типа T | `let values: array<int> = [1, 2, 3];` |
| `map<K, V>` | Ассоциативный массив | `let balances: map<address, uint> = {};` |
| `struct` | Пользовательский составной тип | `struct Token { name: string, symbol: string }` |
| `enum` | Перечисление | `enum Status { Pending, Active, Completed }` |

## Структура контракта

```
contract TokenContract {
    // Объявление состояния контракта (хранится в блокчейне)
    state {
        owner: address;
        total_supply: uint;
        balances: map<address, uint>;
    }
    
    // Конструктор - вызывается один раз при развертывании
    constructor(initial_supply: uint) {
        owner = msg.sender;
        total_supply = initial_supply;
        balances[owner] = initial_supply;
    }
    
    // Функции - могут изменять состояние
    function transfer(to: address, amount: uint) returns bool {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(to != address(0), "Invalid recipient");
        
        balances[msg.sender] -= amount;
        balances[to] += amount;
        
        emit Transfer(msg.sender, to, amount);
        return true;
    }
    
    // Просмотры - не изменяют состояние, только возвращают данные
    view function balance_of(account: address) returns uint {
        return balances[account];
    }
    
    // События - записываются в блокчейн, но не хранятся в состоянии
    event Transfer(from: address, to: address, amount: uint);
}
```

## Управляющие структуры

### Условные операторы

```
if (условие) {
    // код
} else if (другое условие) {
    // код
} else {
    // код
}
```

### Циклы

```
// Цикл for
for (let i: uint = 0; i < 10; i += 1) {
    // код
}

// Цикл while
while (условие) {
    // код
}

// Цикл foreach для итерации по коллекциям
foreach (item in collection) {
    // код
}
```

### Обработка ошибок

```
// Проверка условия и прерывание выполнения при ошибке
require(условие, "Сообщение об ошибке");

// Проверка и откат транзакции при ошибке 
assert(условие, "Сообщение об ошибке");

// Вызов ошибки вручную
revert("Сообщение об ошибке");

// Обработка ошибок (на уровне VM)
try {
    // код, который может вызвать ошибку
} catch (error) {
    // обработка ошибки
}
```

## Взаимодействие с блокчейном

### Глобальные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `block.height` | `uint` | Текущая высота блока |
| `block.timestamp` | `uint` | Временная метка текущего блока |
| `block.difficulty` | `uint` | Сложность текущего блока |
| `msg.sender` | `address` | Адрес отправителя текущей транзакции |
| `msg.value` | `uint` | Сумма GRS, отправленная с текущей транзакцией |
| `tx.hash` | `hash` | Хеш текущей транзакции |
| `contract.address` | `address` | Адрес текущего контракта |
| `contract.balance` | `uint` | Баланс текущего контракта |

### Взаимодействие с другими контрактами

```
// Объявление интерфейса другого контракта
interface ERC20 {
    function transfer(to: address, amount: uint) returns bool;
    view function balance_of(account: address) returns uint;
}

// Использование внешнего контракта
let token: ERC20 = ERC20(token_address);
let success: bool = token.transfer(recipient, amount);
```

## Безопасность и ограничения

1. **Ограничение газа**: каждая операция потребляет определенное количество газа (вычислительных ресурсов)
2. **Ограничение размера хранилища**: контракты имеют ограничение на объем хранимых данных
3. **Предотвращение повторного входа**: автоматическая защита от атак повторного входа
4. **Изоляция выполнения**: контракты не могут вмешиваться в работу друг друга
5. **Детерминированность**: недетерминированные операции (случайные числа, время) ограничены контролируемыми источниками

## Примеры контрактов

### Простой токен

```
contract SimpleToken {
    state {
        name: string;
        symbol: string;
        decimals: uint;
        total_supply: uint;
        balances: map<address, uint>;
    }
    
    constructor(name: string, symbol: string, decimals: uint, initial_supply: uint) {
        self.name = name;
        self.symbol = symbol;
        self.decimals = decimals;
        total_supply = initial_supply;
        balances[msg.sender] = initial_supply;
    }
    
    function transfer(to: address, amount: uint) returns bool {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        balances[to] += amount;
        
        emit Transfer(msg.sender, to, amount);
        return true;
    }
    
    view function balance_of(account: address) returns uint {
        return balances[account];
    }
    
    event Transfer(from: address, to: address, amount: uint);
}
```

### Простой маркетплейс

```
contract Marketplace {
    struct Item {
        id: uint;
        seller: address;
        name: string;
        description: string;
        price: uint;
        available: bool;
    }
    
    state {
        owner: address;
        items: map<uint, Item>;
        next_item_id: uint;
        platform_fee: uint; // в процентах (1 = 0.01%)
    }
    
    constructor(platform_fee: uint) {
        owner = msg.sender;
        next_item_id = 1;
        self.platform_fee = platform_fee;
    }
    
    function list_item(name: string, description: string, price: uint) returns uint {
        let item_id: uint = next_item_id;
        
        items[item_id] = Item {
            id: item_id,
            seller: msg.sender,
            name: name,
            description: description,
            price: price,
            available: true
        };
        
        next_item_id += 1;
        emit ItemListed(item_id, msg.sender, price);
        
        return item_id;
    }
    
    function buy_item(item_id: uint) payable returns bool {
        require(items.contains(item_id), "Item does not exist");
        require(items[item_id].available, "Item is not available");
        require(msg.value >= items[item_id].price, "Insufficient payment");
        
        let item: Item = items[item_id];
        item.available = false;
        items[item_id] = item;
        
        let fee: uint = (item.price * platform_fee) / 10000;
        let seller_amount: uint = item.price - fee;
        
        // Переводим средства продавцу и комиссию владельцу платформы
        transfer_grs(item.seller, seller_amount);
        transfer_grs(owner, fee);
        
        // Возвращаем излишек оплаты
        if (msg.value > item.price) {
            transfer_grs(msg.sender, msg.value - item.price);
        }
        
        emit ItemSold(item_id, item.seller, msg.sender, item.price);
        return true;
    }
    
    view function get_item(item_id: uint) returns Item {
        require(items.contains(item_id), "Item does not exist");
        return items[item_id];
    }
    
    // Только владелец может изменить комиссию
    function set_platform_fee(new_fee: uint) {
        require(msg.sender == owner, "Only owner can change fee");
        require(new_fee <= 1000, "Fee too high"); // Максимальная комиссия 10%
        platform_fee = new_fee;
        emit PlatformFeeChanged(new_fee);
    }
    
    // Внутренняя функция для перевода GRS
    private function transfer_grs(to: address, amount: uint) {
        // Низкоуровневый вызов для перевода нативной криптовалюты
        native.transfer(to, amount);
    }
    
    event ItemListed(item_id: uint, seller: address, price: uint);
    event ItemSold(item_id: uint, seller: address, buyer: address, price: uint);
    event PlatformFeeChanged(new_fee: uint);
}
```

## Версионирование

Grishex поддерживает версионирование контрактов. В начале каждого файла можно указать версию языка:

```
pragma grishex 1.0;

contract MyContract {
    // ...
}
```

## Компиляция и развертывание

Контракты Grishex компилируются в байткод для виртуальной машины Grishinium (GVM) с помощью компилятора `grishexc`:

```bash
grishexc token.gx --output token.gvm
```

Развертывание осуществляется с помощью транзакции специального типа в блокчейне Grishinium. 