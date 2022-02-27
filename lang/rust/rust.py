import re

from talon import Context, Module, actions, settings

mod = Module()
ctx = Context()
ctx.matches = r"""
tag: user.python
"""

standard_macros = {
    "panic": "panic!",
    "format": "format!",
    "concatenate": "concat!",
    "print": "print!",
    "print line": "println!",
}

logging_macros = {
    "debug": "debug!",
    "info": "info!",
    "warning": "warn!",
    "error": "error!",
}

testing_macros = {
    "assert": "assert!",
    "assert equal": "assert_eq!",
    "assert not equal": "assert_ne!",

}

# tag: functions_gui
ctx.lists["user.code_functions"] = {
    **standard_macros,
    **logging_macros,
    **testing_macros,
}

scalar_types = {
    "eye 8": "i8",
    "you 8": "u8",
    "bytes": "u8",
    "eye 16": "i16",
    "you 16": "u16",
    "eye 32": "i32",
    "you 32": "u32",
    "eye 64": "i64",
    "you 64": "u64",
    "eye 128": "i128",
    "you 128": "u128",
    "eye size": "isize",
    "you size": "usize",
    "float 32": "f32",
    "float 64": "f64",
    "boolean": "bool",
    "character": "char",
}

compound_types = {
    "tuple": "()",
    "array": "[]",
}

standard_library_types = {
    "box": "Box",
    "vector": "Vec",
    "string": "String",
    "string slice": "&str",
    "os string": "OsString",
    "os string slice": "&OsStr",
    "see string": "CString",
    "see string slice": "&CStr",
    "option": "Option",
    "result": "Result",
    "hashmap": "HashMap",
    "hash set": "HashSet",
    "reference count": "Rc",
}

standard_sync_types = {
    "arc": "Arc",
    "barrier": "Barrier",
    "condition variable": "Condvar",
    "mutex": "Mutex",
    "once": "Once",
    "read write lock": "RwLock",
    "receiver": "Receiver",
    "sender": "Sender",
    "sink sender": "SyncSender",
}

# tag: functions
ctx.lists["user.code_type"] = {
    **scalar_types,
    **compound_types,
    **standard_library_types,
    **standard_sync_types,
}

@ctx.action_class("user")
class UserActions:

    # tag: comment_line

    def code_comment_line_prefix():
        actions.insert('// ')

    # tag: comment_block

    def code_comment_block():
        actions.insert('/*')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()

    def code_comment_block_prefix():
        actions.auto_insert('/*')

    def code_comment_block_suffix():
        actions.auto_insert('*/')

    # tag: comment_documentation

    def code_comment_documentation():
        actions.insert('/// ')

    def code_comment_documentation_block():
        actions.insert('/**')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')
        actions.edit.up()

    def code_comment_documentation_inner():
        actions.insert('//! ')

    def code_comment_documentation_block_inner():
        actions.insert('/*!')
        actions.key('enter')
        actions.key('enter')
        actions.insert('*/')

    # tag: imperative

    def code_block():
        actions.insert("{}")
        actions.key("left enter")

    def code_state_if():
        actions.insert('if  {\n}\n')
        actions.key('up:2 left:2')

    def code_state_else_if():
        actions.insert('else if  {\n}\n')
        actions.key('up:2 left:2')

    def code_state_else():
        actions.insert('else\n{\n}\n')
        actions.key('up:2')

    def code_state_switch():
        actions.insert('match  {\n}\n')
        actions.key('up:2 left:2')

    def code_state_for():
        actions.insert('for  in  {\n}\n')
        actions.key('up:2 left:6')

    def code_state_for_each():
        actions.insert('for  in  {\n}\n')
        actions.key('up:2 left:6')

    def code_state_while():
        actions.insert('while  {\n}\n')
        actions.key('up:2 left:2')

    def code_state_loop():
        actions.insert('loop  {\n}\n')
        actions.key('up:2 left:2')

    def code_state_return():
        actions.auto_insert('return ')

    def code_break():
        actions.auto_insert('break;')

    def code_next():
        actions.auto_insert('continue;')

    # tag: object_oriented

    def code_operator_object_accessor():
        actions.auto_insert('.')

    def code_self():
        actions.auto_insert('self')

    def code_define_class():
        actions.auto_insert('struct ')

    # tag: data_bool

    def code_insert_true():
        actions.auto_insert('true')

    def code_insert_false():
        actions.auto_insert('false')

    # tag: data_null
    # Convenience function, however, Option technically isn't null

    def code_insert_null():
        actions.auto_insert('None')

    def code_insert_is_null():
        actions.auto_insert('.is_none()')

    def code_insert_is_not_null():
        actions.auto_insert('.is_some()')

    # tag: functions

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_private_function(text: str):
        result = "fn {}() {{\n}}\n".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.key('up:2 left:3')

    def code_public_function(text: str):
        result = "pub fn {}() {{\n}}\n".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.paste(result)
        actions.key('up:2 left:3')

    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" -> {type}")

    # tag: functions_gui

    def code_insert_function(text: str, selection: str):
        if selection:
            out_text = text + "({})".format(selection)
        else:
            out_text = text + "()"
        actions.user.paste(out_text)
        actions.edit.left()

    # tag: libraries

    def code_import():
        actions.auto_insert('use ')

    # tag: libraries_gui

    def code_insert_library(text: str, selection: str):
        actions.user.paste("use {}".format(selection))

    # tag: operators_array

    def code_operator_subscript():
        actions.insert('[]')
        actions.key('left')

    # tag: code_operators_assignment

    def code_operator_assignment():
        actions.auto_insert(' = ')

    def code_operator_subtraction_assignment():
        actions.auto_insert(' -= ')

    def code_operator_addition_assignment():
        actions.auto_insert(' += ')

    def code_operator_multiplication_assignment():
        actions.auto_insert(' *= ')

    def code_operator_division_assignment():
        actions.auto_insert(' /= ')

    def code_operator_modulo_assignment():
        actions.auto_insert(' %= ')

    def code_operator_bitwise_and_assignment():
        actions.auto_insert(' &= ')

    def code_operator_bitwise_or_assignment():
        actions.auto_insert(' |= ')

    def code_operator_bitwise_exclusive_or_assignment():
        actions.auto_insert(' ^= ')

    def code_operator_bitwise_left_shift_assignment():
        actions.auto_insert(' <<= ')

    def code_operator_bitwise_right_shift_assignment():
        actions.auto_insert(' >>= ')

    # tag: operators_bitwise

    def code_operator_bitwise_and():
        actions.auto_insert(' & ')

    def code_operator_bitwise_or():
        actions.auto_insert(' | ')

    def code_operator_bitwise_exclusive_or():
        actions.auto_insert(' ^ ')

    def code_operator_bitwise_left_shift():
        actions.auto_insert(' << ')

    def code_operator_bitwise_right_shift():
        actions.auto_insert(' >> ')

    # tag: operators_math

    def code_operator_subtraction():
        actions.auto_insert(' - ')

    def code_operator_addition():
        actions.auto_insert(' + ')

    def code_operator_multiplication():
        actions.auto_insert(' * ')

    def code_operator_exponent():
        actions.auto_insert('.pow()')
        actions.key('left')

    def code_operator_division():
        actions.auto_insert(' / ')

    def code_operator_modulo():
        actions.auto_insert(' % ')

    def code_operator_equal():
        actions.auto_insert(' == ')

    def code_operator_not_equal():
        actions.auto_insert(' != ')

    def code_operator_greater_than():
        actions.auto_insert(' > ')

    def code_operator_greater_than_or_equal_to():
        actions.auto_insert(' >= ')

    def code_operator_less_than():
        actions.auto_insert(' < ')

    def code_operator_less_than_or_equal_to():
        actions.auto_insert(' <= ')

    def code_operator_and():
        actions.auto_insert(' && ')

    def code_operator_or():
        actions.auto_insert(' || ')

    # tag: operators_pointer

    def todo():
        todo!()
