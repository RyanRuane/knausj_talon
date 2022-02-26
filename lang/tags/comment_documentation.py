from talon import Context, Module

ctx = Context()
mod = Module()

mod.tag("code_comment_documentation", desc="Tag for enabling generic documentation commands")
mod.tag("code_comment_documentation_block", desc="Tag for enabling generic block documentation commands")
mod.tag("code_comment_documentation_inner", desc="Tag for enabling generic inner documentation commands")
mod.tag("code_comment_documentation_block_inner", desc="Tag for enabling generic inner block documentation commands")


@mod.action_class
class Actions:

    def code_comment_documentation():
        """Inserts a document comment and positions the cursor appropriately"""

    def code_comment_documentation_block():
        """Inserts a block document comment and positions the cursor appropriately"""

    def code_comment_documentation_inner():
        """Inserts an inner document comment and positions the cursor appropriately"""

    def code_comment_documentation_block_inner():
        """Inserts an inner block document comment and positions the cursor appropriately"""
