# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import re
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, datetime


# Krijimi i klases Pacienti

class Pacienti(models.Model):

    _name = "spital.pacienti"
    _description = "Pacienti"
    _order = "name"

    nr_personal = fields.Char(string="Nr. personal", required=True)
    name = fields.Char(string="Emri", required=True)
    amesia = fields.Char(string="Amësia", required=True)
    atesia = fields.Char(string="Atësia", required=True)
    ditelindja = fields.Date(string="Ditëlindja", required=True)
    gjinia = fields.Selection([
        ('mashkull', 'Mashkull'),
        ('femer', 'Femër')
    ], string="Gjinia", required=True)
    gjendja_civile = fields.Selection([
        ('beqar', 'Beqar/e'),
        ('martuar', 'I/E martuar'),
        ('divorcuar', 'I/E divorcuar'),
        ('ve', 'I/E ve')
    ], string="Gjendja Civile")
    grupi_gjakut = fields.Selection(
        [('0+', '0+'), ('0-', '0-'), ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-')],
        string="Grupi i gjakut")
    vendlindja = fields.Char(string="Vendlindja")
    adresa = fields.Text(string="Adresa")
    cel = fields.Char(string="Nr. kontakti")
    email = fields.Char(string="E-mail")
    diagnoza_pacient = fields.One2many('spital.konsulta', 'pacient_id', string="Diagnoza")

   # Kontrollon nese nr personal eshte unik.
    _sql_constraints = [
        ('nr_personal_unik', 'unique(nr_personal)', "Numri personal është unik për çdo individ!"),
    ]

   # Kontrollon nese nr personal ka 10 char.
    @api.constrains('nr_personal')
    def _nr_personal_length(self):
        if (len(self.nr_personal) != 10):
            raise ValidationError("Numri personal duhet të jetë me 10 karaktere!")

    # Kontrollon nese adresa e email eshte e vlefshme.
    @api.constrains('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Ju lutem vendosni një adresë e-mail të vlefshme!')

    # Kontrollon qe fusha 'cel' te mbaje vetem numra.
    @api.constrains('cel')
    def validate_cel(self):
        if self.cel:
            if not self.cel.isdigit():
                raise ValidationError('Numri i kontaktit duhet të përmbajë vetëm numra!')

# ----------------------------------------------------------------------------------------------------------------------

# Krijimi i klases Doktori

class Doktori(models.Model):

    _name = "spital.doktori"
    _description = "Doktori"
    _order = "name"

    #Info rreth punes
    departamenti = fields.Many2one('spital.departamenti', 'Departamenti')
    zyra = fields.Char(string="Zyra")
    cel_pune = fields.Char(string="Nr. kontakti")
    email_pune = fields.Char(string="E-mail")
    specializim = fields.One2many('spital.specializimi', 'doktor_id', string="Specializimet")
    specializimi_fundit = fields.Text(compute='_specializimi_fundit', string="Specializimi i fundit")
    statusi_dok = fields.Selection([
        ('disponueshem', 'I disponueshëm'),
        ('padisponueshem', 'I padisponueshëm'),
        ('zene', 'I zënë')
    ], string="Statusi i Doktorit", default="disponueshem")

    #Info personal
    nr_personal = fields.Char(string="Nr. personal", required=True)
    name = fields.Char(string="Emri", required=True)
    atesia = fields.Char(string="Atësia", required=True)
    gjinia = fields.Selection([
        ('mashkull', 'Mashkull'),
        ('femer', 'Femër')
    ], string="Gjinia", required=True)
    gjendja_civile = fields.Selection([
        ('beqar', 'Beqar/e'),
        ('martuar', 'I/E martuar'),
        ('divorcuar', 'I/E divorcuar'),
        ('ve', 'I/E ve')
    ], string="Gjendja Civile")
    ditelindja = fields.Date('Ditëlindja', required=True)
    grupi_gjakut = fields.Selection(
        [('0+', '0+'), ('0-', '0-'), ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'),
         ('ab-', 'AB-')],
        string="Grupi i gjakut")
    vendlindja = fields.Char(string="Vendlindja")
    adresa = fields.Text(string="Adresa")
    cel_personal = fields.Char(string="Nr. kontakti personal")
    email_personal = fields.Char(string="E-mail personal")

    # Kontrollon nese nr. personal eshte unik.
    _sql_constraints = [
        ('nr_personal_unik_dok', 'unique(nr_personal)', "Numri personal është unik për çdo individ!"),
    ]

    # Kontrollon nese nr personal ka 10 char.
    @api.constrains('nr_personal')
    def _nr_personal_length(self):
        if (len(self.nr_personal) != 10):
            raise ValidationError("Numri personal duhet të jetë me 10 karaktere!")

    # Kontrollon nese adresa e email e punes eshte e vlefshme.
    @api.constrains('email_pune')
    def validate_mail_pune(self):
        if self.email_pune:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_pune)
            if match == None:
                raise ValidationError('Ju lutem vendosni një adresë e-mail të vlefshme!')

    # Kontrollon nese adresa e email personale eshte e vlefshme.
    @api.constrains('email_personal')
    def validate_mail_personal(self):
        if self.email_personal:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_personal)
            if match == None:
                raise ValidationError('Ju lutem vendosni një adresë e-mail të vlefshme!')

    # Kontrollon qe fusha 'cel_pune' te mbaje vetem numra.
    @api.constrains('cel_pune')
    def validate_cel_pune(self):
        if self.cel_pune:
            if not self.cel_pune.isdigit():
                raise ValidationError('Numri i kontaktit duhet të përmbajë vetëm numra!')

    # Kontrollon qe fusha 'cel_personal' te mbaje vetem numra.
    @api.constrains('cel_personal')
    def validate_cel_personal(self):
        if self.cel_personal:
            if not self.cel_personal.isdigit():
                raise ValidationError('Numri i kontaktit duhet të përmbajë vetëm numra!')

    # Llogarit vleren e fushes 'specializimi_fundit', duke gjetur specializimin me date me te vone.
    @api.multi
    def _specializimi_fundit(self):
        for record in self:
            if record.specializim:
                data_fundit = datetime.now()
                DATETIME_FORMAT = "%Y-%m-%d"
                for el in record.specializim:
                    if datetime.strptime(el.data, DATETIME_FORMAT) < data_fundit:
                        data_fundit = datetime.strptime(el.data, DATETIME_FORMAT)
                        special_fundit = el.name
                record.specializimi_fundit = special_fundit

# ----------------------------------------------------------------------------------------------------------------------

# Krijimi i klases Specializimi

class Specializimi (models.Model):
    _name = "spital.specializimi"
    _description = "Specializimet"

    name = fields.Text(string="Specializimi")
    data = fields.Date(string="Data", required=True)
    doktor_id = fields.Many2one('spital.doktori', string="Mjeku")

# ----------------------------------------------------------------------------------------------------------------------

# Krijimi i klases Departamenti

class Departamenti (models.Model):
    _name = "spital.departamenti"
    _description = "Departamenti"
    _order = "name"

    name = fields.Char(string="Departamenti", required=True)
    krye_mjek = fields.Char(string="Krye Mjeku")

# ----------------------------------------------------------------------------------------------------------------------

# Krijimi i klases Konsulta

class Konsulta (models.Model):
    _name = "spital.konsulta"
    _description = "Konsulta"
    _order = "date_fillimi desc"

    pacient_id = fields.Many2one('spital.pacienti', string="Pacienti")
    mjek_id = fields.Many2one('spital.doktori', string="Doktori", required=True)
    dep_id = fields.Many2one('spital.departamenti', string="Departamenti", required=True)
    date_fillimi = fields.Datetime(string="Data/Ora e fillimit", default=lambda self: fields.datetime.now())
    date_perfundimi = fields.Datetime(string="Data/Ora e përfundimit")
    simptoma = fields.Text(string="Simptomat")
    name = fields.Char(string="Diagnoza")
    trajtimi = fields.Text(string="Trajtimi")
    shenim = fields.Text(string="Shënim")
    statusi_kons = fields.Selection([
        ('planifikuar', 'Planifikuar'),
        ('konsulte', 'Konsultë'),
        ('perfunduar', 'Përfunduar')
    ], string="Statusi i Konsultës", default="planifikuar", required=True)
    konsulte = fields.Boolean(string="Konsultë", default=False)

   # I jep vlere automatikisht dates se perfundimit te konsultes, duke i shtuar 30 min dates se fillimit.
    @api.onchange('date_fillimi')
    def _onchange_time(self):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.date_perfundimi = datetime.strptime(self.date_fillimi, DATETIME_FORMAT) + timedelta(minutes=30)

    # Ndryshon statusin e doktorit pasi ndryshohet statusi i konsultes.
    # Statusi i konsultes ndryshohet manualisht nga nje person pergjegjes.
    @api.onchange('statusi_kons')
    def onchange_statusi(self):
        for record in self:
            if record.statusi_kons:
                if record.statusi_kons == 'konsulte':
                    record.mjek_id.write({'statusi_dok':'zene'})
                elif record.statusi_kons == 'perfunduar':
                    record.mjek_id.write({'statusi_dok':'disponueshem'})

    # Duhet te check-ohet patjeter fusha Konsulte, ne menyre qe ajo te marre vleren True.
    # Kjo do te na sherbeje per te bere dallimin mes konsultes dhe padisponueshmerise se mjekut.
    @api.constrains('konsulte')
    def _check_konsulte(self):
        if (self.pacient_id and self.konsulte == False):
            raise ValidationError("Ju lutem klikoni fushën 'Konsultë'!")

    # Kontrollon nese ka perplasje oraresh kur rezervohet nje konsulte e re.
    @api.model
    def create(self, values):
        if values.get('mjek_id', False) and values.get('date_fillimi', False) and values.get('date_perfundimi', False):
            ids = self.search([('mjek_id', '=', values['mjek_id'])])
            if ids:
                ids1 = ids.search(['&', ('date_fillimi', '<=', values['date_fillimi']), ('date_perfundimi', '>=', values['date_fillimi'])])
                ids2 = ids.search(['&', ('date_fillimi', '<=', values['date_perfundimi']), ('date_perfundimi', '>=', values['date_perfundimi'])])
                if (ids1 or ids2):
                    raise UserError(_("Doktori nuk është i disponueshëm në këtë orar!"))
        return super(Konsulta, self).create(values)

    # Kontrollon nese ka perplasje oraresh kur perditesohet nje konsulte e rezervuar.
    @api.multi
    def write(self, vals):
        if vals.get('mjek_id', False) and vals.get('date_fillimi', False) and vals.get('date_perfundimi', False):
            wids = self.search([('mjek_id', '=', vals['mjek_id'])])
            if wids:
                wids1 = wids.search(['&', ('date_fillimi', '<=', vals['date_fillimi']), ('date_perfundimi', '>=', vals['date_fillimi'])])
                wids2 = wids.search(['&', ('date_fillimi', '<=', vals['date_perfundimi']), ('date_perfundimi', '>=', vals['date_perfundimi'])])
                if (wids1 or wids2):
                    raise UserError(_("Doktori nuk është i disponueshëm në këtë orar!"))
        return super(Konsulta, self).write(vals)

    # Nuk lejon fshirjen e konsultave qe jane ne statusin 'konsulte' ose 'perfunduar'.
    @api.multi
    def unlink(self):
        for konsulte in self:
            if konsulte.statusi_kons in ('konsulte', 'perfunduar'):
                raise UserError(_("Nuk mund të fshish një konsultë që është në statusin 'konsultë' ose 'përfunduar'!"))
        return super(Konsulta, self).unlink()








