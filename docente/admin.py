from django.contrib import admin
from .models import Ejercicio, Tema, Subtema
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.formats.base_formats import CSV

# --------------------------
# Resource para Ejercicio
# --------------------------
class EjercicioResource(resources.ModelResource):
    class Meta:
        model = Ejercicio
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # Convertir nombres de Tema y Subtema a IDs
        if 'tema' in row and row['tema']:
            tema_obj = Tema.objects.filter(nombre=row['tema']).first()
            if tema_obj:
                row['tema'] = tema_obj.id
            else:
                tema_obj = Tema.objects.create(nombre=row['tema'])
                row['tema'] = tema_obj.id

        if 'subtema1' in row and row['subtema1']:
            sub1_obj = Subtema.objects.filter(nombre=row['subtema1']).first()
            if sub1_obj:
                row['subtema1'] = sub1_obj.id
            else:
                sub1_obj = Subtema.objects.create(nombre=row['subtema1'])
                row['subtema1'] = sub1_obj.id

        if 'subtema2' in row and row['subtema2']:
            sub2_obj = Subtema.objects.filter(nombre=row['subtema2']).first()
            if sub2_obj:
                row['subtema2'] = sub2_obj.id
            else:
                sub2_obj = Subtema.objects.create(nombre=row['subtema2'])
                row['subtema2'] = sub2_obj.id

    def export(self, queryset=None, *args, **kwargs):
        dataset = super().export(queryset, *args, **kwargs)
        dataset.csv_delimiter = ';'  # Forzar delimitador
        return dataset

# --------------------------
# Admin para Ejercicio
# --------------------------
@admin.register(Ejercicio)
class EjercicioAdmin(ImportExportModelAdmin):
    resource_class = EjercicioResource

    def get_export_formats(self):
        formats = super().get_export_formats()
        for f in formats:
            if isinstance(f, CSV):
                f.delimiter = ';'  # Forzar delimitador
        return formats

# --------------------------
# Admin para Tema
# --------------------------
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)

# --------------------------
# Admin para Subtema
# --------------------------
@admin.register(Subtema)
class SubtemaAdmin(admin.ModelAdmin):
    search_fields = ("nombre", "tema__nombre")
