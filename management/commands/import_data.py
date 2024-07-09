from django.core.management.base import BaseCommand
from dbfread import DBF
from database.inventory.models import Hardware, Model, EquipmentType

class Command(BaseCommand):
    help = 'Import data from DBF files into Django models'

    def handle(self, *args, **kwargs):
        # Пути к вашим DBF файлам
        hardware_dbf = "database/dbfiles/HARDWARE.DBF"
        model_dbf = "database/dbfiles/MODEL.DBF"
        typeequip_dbf = "database/dbfiles/TYPEEQU.DBF"

        # Очистить существующие данные при необходимости
        Hardware.objects.all().delete()
        Model.objects.all().delete()
        EquipmentType.objects.all().delete()

        # Импорт EquipmentType
        typeequip_table = DBF(typeequip_dbf, ignore_missing_memofile=True)
        for record in typeequip_table:
            EquipmentType.objects.create(name=record['NAME'])

        # Импорт Model
        typeequip_dict = {record['TYPEEQUID']: record['NAME'] for record in typeequip_table}
        model_table = DBF(model_dbf, ignore_missing_memofile=True)
        for record in model_table:
            equipment_type = EquipmentType.objects.get(name=typeequip_dict.get(record['TYPEEQUID']))
            Model.objects.create(name=record['NAME'], equipment_type=equipment_type)

        # Импорт Hardware
        models_dict = {record['MODELID']: record for record in model_table}
        hardware_table = DBF(hardware_dbf, ignore_missing_memofile=True)
        for record in hardware_table:
            model_record = models_dict.get(record['MODELID'])
            model = Model.objects.get(name=model_record['NAME'])
            Hardware.objects.create(
                sn=record['SN'],
                inventn=record['INVENTN'],
                created=record['CREATED'],
                model=model
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))