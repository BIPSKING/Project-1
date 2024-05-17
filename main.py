from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.list import ThreeLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
import taskmanager as TM
from jnius import autoclass

# Dialog box class
class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
        self.ids.time_text.text = str(datetime.now().strftime('%H:%M'))

    # function for date dialog picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def show_time_picker(self):
        default_time = datetime.strptime('00:00', '%H:%M').time()

        time_dialog = MDTimePicker()
        time_dialog.set_time(default_time)
        time_dialog.bind(on_save=self.get_time)
        time_dialog.open()

    def get_time(self, instance, value):
        time = value.strftime('%H:%M')
        self.ids.time_text.text = str(time)

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # mark the task as complete or incomplete
    def mark(self, check, the_list_item):
        if check.active:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            TM.task_complete(self.pk)
        else:
            the_list_item.text = TM.task_incomplete(self.pk)

    def delete_item(self, the_list_item):
        TM.pop_task(self.pk)
        self.parent.remove_widget(the_list_item)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

# Main App class
class ReMindApp(MDApp):
    task_list_dialog = None

    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Orange"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )
        self.task_list_dialog.open()

    def on_start(self):
        load_bool = TM.list_store()
        if load_bool:
            stored_task_items = TM.load_tasks()
            for item in stored_task_items:
                self.add_list_item(item)
        else:
            pass

    def on_stop(self):
        TM.sort_id()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date, task_time):
        TM.add_task(task.text, task_date, task_time)
        task_items = TM.get_tasks()
        self.add_list_item(task_items)
        task.text = ''

    def add_list_item(self, item):
        if item[4]:
            add_task = ListItemWithCheckbox(
                pk=item[0],
                text='[s]' + str(item[1]) + '[/s]',
                secondary_text=item[2],
                tertiary_text=item[3]
            )
            add_task.ids.check.active = True
        else:
            add_task = ListItemWithCheckbox(
                pk=item[0],
                text=str(item[1]),
                secondary_text=item[2],
                tertiary_text=item[3]
            )
        self.root.ids.container.add_widget(add_task)

    def start_service(self):
        service = autoclass('org.kivy.android.PythonService')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')

if __name__ == '__main__':
    app = ReMindApp()
    app.run()
