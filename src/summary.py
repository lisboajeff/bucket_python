from usecases.action import Action
from usecases.info import Information


class SummaryVisitor:

    def report_without_actions(self) -> str:
        pass

    def title(self) -> str:
        pass

    def uploaded_message(self) -> str:
        pass

    def remove_message(self) -> str:
        pass

    def action(self) -> str:
        pass


class Summary(Action):

    def __init__(self, filename: str, visitor: SummaryVisitor):
        self.actions: dict[str, list[Information]] = {"Uploaded": [], "Removed": []}
        self.filename: str = filename
        self.visitor = visitor

    def _format_summary(self) -> list[str]:
        lines: list[str] = [self.visitor.title()]
        if not self.actions["Uploaded"] and not self.actions["Removed"]:
            lines.append(self.visitor.report_without_actions())
        else:
            lines.append(f"| {self.visitor.action()} | File Name | Old Hash | New Hash |")
            lines.append("|---| ---  |---| ---")
            for info in self.actions["Uploaded"]:
                lines.append(
                    f"| {self.visitor.uploaded_message()}  |  {info.get_file_path()} "
                    f"| {info.get_old_hash()} | {info.get_hash()} |")
            for info in self.actions["Removed"]:
                lines.append(
                    f"| {self.visitor.remove_message()} | {info.get_file_path()} "
                    f"| {info.get_old_hash()} | {info.get_hash()} |")

        return lines

    def export(self):
        text = self._format_summary()
        print("\n".join(text))
        with open(self.filename, "w") as file:
            file.write("\n".join(text))

    def insert_uploaded(self, information: Information):
        self.actions["Uploaded"].append(information)

    def insert_removed(self, information: Information):
        self.actions["Removed"].append(information)
