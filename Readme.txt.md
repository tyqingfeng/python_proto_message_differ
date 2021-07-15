一个ProtoBuf 协议文件比较工具，通过比较协议文件，生成diff 报告，显示协议字段差异，缺失字段等。

### 背景

项目规模较大时，协议文件越来越大，客户端在多个module中可能存在多份协议文件；通常云端维护一份协议文件，两者定义协议message 的顺序也不一致。

持续开发过程中，存在客户端侧协议文件和云端不同步导致的业务问题甚至crash 问题。 

协议过大时，人工比较成功过高，通过工具便捷输出协议差异，给予提示。

### ProtoBuf 协议格式

```javascript
字段格式：限定修饰符① | 数据类型② | 字段名称③ | = | 字段编码值④ | [字段默认值⑤]
```

如：

```none
syntax = "proto3";

package tutorial; // 定义作用域

message Person {        // 生成类class Person : public ::google::protobuf::Message 
  required string name = 1;
  required int32 id = 2;
  optional string email = 3;

  enum PhoneType { 
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber { 
    required string number = 1;
    optional PhoneType type = 2 [default = HOME];
  }
  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```

### Usage使用

##### 配置选项

```
class Config(object):
    # 日志
    IS_PRINT_LOG = True
    IS_PRINT_RESULT_LOG = True
    IS_PRINT_INC_FIELD = False
    IS_PRINT_FIELD_DETAIL_INFO = False
    IS_PRINT_FIELD_TYPE_DIS_MATCH = True

    # 测试配置
    IS_PRINT_LOG = False
    MESSAGE_FILE_PATH = "msg.txt"
    MESSAGE_FILE_1_PATH = "msg1.txt"
    CMP_MESSAGE_FILE_PATH = "msg_compare.txt"

    # 是否匹配字段的缺失
    MATCH_IS_CATCH_LEAK_FIELD = False
    # 是否只匹配由于类型不一致引起的diff；忽略其他原因
    MATCH_IS_CATCH_OTHER_DISMISS_TYPE = False
    # 不匹配类型， 如int32 和 string； 如协议中定义的枚举，在其他协议中为int类型
    MATCH_IS_IGNORE_TYPE = False
    MATCH_IS_IGNORE_PACKAGE_NAME = True  # 忽略包名
    # 强制匹配部分类型
    MATCH_IS_MAKE_BYTES_STRING_EQUAL = False

    # 输出结构
    OUTPUT_FILE_NAME = "result_1.txt"
    OUTPUT_BRIEF_FILE_NAME = "brief_result_1.txt"
    OUTPUT_FILE_2_NAME = "result_2.txt"
    OUTPUT_BRIEF_FILE_2_NAME = "brief_result_2.txt"

    # 语法词
    SYNTAX_WORDS = ["optional", "repeated", "required"]
    # 定义message 名称不同，实际为一个协议时，使用匿名方式比较
    ALIAS_DICT = {
        "AddressBookAlias": "AddressBook"
    }
```

经过配置后，运行main.py   main函数。

### Diff结果

输出简略比较结果和详细比较结果，如下：

示例 result_1.txt

```
message Person
optional int32 id = 2;    //required表示必须有，否则为uninitialized，parse时候会失败        被比较字段:  required string id = 2;    //required表示必须有，否则为uninitialized，parse时候会失败
optional string email = 3;    //option表示可以没有，他们都有default value        被比较字段:  required string email = 3;    //option表示可以没有，他们都有default value
  
message PhoneNumber
optional PhoneType type = 2 [default = HOME];        被比较字段:    optional int32 type = 2 [default = HOME];
```

示例 brief_result_1.txt， 仅输出message 名称

```
diff1
Person
PhoneNumber
```

### 结构划分

1. 定义消息字段包含语法字段，名称，所以，类型，内容，提供消息比较，alias比较； 定义消息体，存储消息字段map
2. 定义匹配器，用于进行词法分析，从单行中提取字段，通过定义不同的正则表达式，提取分词信息，如：
reg_str = r"(?P<syntax>("
for syntax_word in self.syntax_words:
reg_str = reg_str + syntax_word + "|"
self.middle_reg = reg_str[:-1] + r")) +(?P<type>[\w.?]+)\s*(?P<name>\w+)\s*= *(?P<index>\d+)"
对外提供不同阶段的匹配函数

3. 定义语法分析器，协议分析定义基础堆栈，使用匹配器来确定状态，结合有限状态和分词内容来进行分析，如确定 proto 协议开始定义，协议嵌套（协议中定义enum；使用外层.内层 层级表达）， 协议结束。
4. 定义消息协议比较器，根据语法分析器生成云端协议和本地协议的消息内容，然后对两份消息内容进行对比，输出差异字段，差异内容所在的协议，行号信息。
5. 配置文件，支持多维度的日志开关，测试文件配置， 匹配选项，如：是否不匹配类型，忽略报名，强制匹配部分类型等， 配置语法分词如：["optional", "repeated", "required"]



可以根据以上划分，进行扩展。