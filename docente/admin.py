from django.contrib import admin
from .models import Tema, Subtema1, Subtema2, Ejercicio
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
        # --- Tema ---
        if 'tema' in row and row['tema']:
            tema_obj, _ = Tema.objects.get_or_create(nombre=row['tema'])
            row['tema'] = tema_obj.id

        # --- Subtema1 ---
        if 'subtema1' in row and row['subtema1']:
            if 'tema' in row and row['tema']:
                tema_obj = Tema.objects.filter(id=row['tema']).first()
            else:
                tema_obj = None
            sub1_obj, _ = Subtema1.objects.get_or_create(nombre=row['subtema1'], tema=tema_obj)
            row['subtema1'] = sub1_obj.id

        # --- Subtema2 ---
        if 'subtema2' in row and row['subtema2']:
            if 'subtema1' in row and row['subtema1']:
                sub1_obj = Subtema1.objects.filter(id=row['subtema1']).first()
            else:
                sub1_obj = None
            sub2_obj, _ = Subtema2.objects.get_or_create(nombre=row['subtema2'], subtema1=sub1_obj)
            row['subtema2'] = sub2_obj.id

    def export(self, queryset=None, *args, **kwargs):
        dataset = super().export(queryset, *args, **kwargs)
        dataset.csv_delimiter = ';'  # Forzar delimitador
        return dataset


# --------------------------
# Admin Ejercicio
# --------------------------
@admin.register(Ejercicio)
class EjercicioAdmin(ImportExportModelAdmin):
    resource_class = EjercicioResource
    list_display = ("id", "nombre", "tema", "subtema1", "subtema2", "momento", "nivel")
    search_fields = ("nombre", "descripcion", "tema__nombre", "subtema1__nombre", "subtema2__nombre")
    list_filter = ("tema", "subtema1", "subtema2", "momento", "nivel")

    def get_export_formats(self):
        formats = super().get_export_formats()
        for f in formats:
            if isinstance(f, CSV):
                f.delimiter = ';'  # Forzar delimitador
        return formats


# --------------------------
# Admin Tema
# --------------------------
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)
    list_display = ("id", "nombre")


# --------------------------
# Admin Subtema1
# --------------------------
@admin.register(Subtema1)
class Subtema1Admin(admin.ModelAdmin):
    search_fields = ("nombre", "tema__nombre")
    list_display = ("id", "nombre", "tema")
    list_filter = ("tema",)


# --------------------------
# Admin Subtema2
# --------------------------
@admin.register(Subtema2)
class Subtema2Admin(admin.ModelAdmin):
    search_fields = ("nombre", "subtema1__nombre", "subtema1__tema__nombre")
    list_display = ("id", "nombre", "subtema1", "get_tema")
    list_filter = ("subtema1__tema", "subtema1")

    def get_tema(self, obj):
        return obj.subtema1.tema
    get_tema.short_description = "Tema"
