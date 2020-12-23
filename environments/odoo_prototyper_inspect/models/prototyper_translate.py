# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo
from odoo import models, api
import os
import logging
from odoo.tools.translate import TranslationFileReader
from odoo.tools.misc import file_open, get_iso_codes

_logger = logging.getLogger(__name__)


class prototyper_translate(models.AbstractModel):
    _name = 'prototyper.translate'
    _description = '翻译'

    _translate_dict = []

    @api.model
    def trans_load(self, filename, lang, verbose=True, module_name=None, context=None):
        try:
            with file_open(filename, mode='rb') as fileobj:
                _logger.info("loading %s", filename)
                fileformat = os.path.splitext(filename)[-1][1:].lower()
                result = self.trans_load_data(
                    fileobj, fileformat, lang, verbose=verbose, module_name=module_name, context=context)
                return result
        except IOError:
            if verbose:
                _logger.error("couldn't read translation file %s", filename)
        return None

    @api.model
    def translate(self, imd_name, name, src, type, lang='zh_CN'):
        if not src:
            return src

        result = src
        for item in self._translate_dict:
            if (item['imd_name'] == imd_name and item['name'] == name and item['src'] == src
                    and item['type'] == type and item['lang'] == lang):
                result = item['value']
        return result

    def trans_load_data(self, fileobj, fileformat, lang, lang_name=None, verbose=True, module_name=None, context=None):
        """Populates the ir_translation table."""
        if verbose:
            _logger.info('loading translation file for language %s', lang)

        env = odoo.api.Environment(self.env.cr, odoo.SUPERUSER_ID, context or {})
        Lang = env['res.lang']
        Translation = env['ir.translation']

        try:
            if not Lang.search_count([('code', '=', lang)]):
                # lets create the language with locale information
                Lang.load_lang(lang=lang, lang_name=lang_name)

            # now, the serious things: we read the language file
            fileobj.seek(0)
            reader = TranslationFileReader(fileobj, fileformat=fileformat)

            # read the rest of the file

            def process_row(row):
                """Process a single PO (or POT) entry."""
                # dictionary which holds values for this line of the csv file
                # {'lang': ..., 'type': ..., 'name': ..., 'res_id': ...,
                #  'src': ..., 'value': ..., 'module':...}
                dic = dict.fromkeys(('type', 'name', 'res_id', 'src', 'value',
                                     'comments', 'imd_model', 'imd_name', 'module'))
                dic['lang'] = lang
                dic.update(row)

                # do not import empty values
                if not env.context.get('create_empty_translation', False) and not dic['value']:
                    return

                if dic['type'] == 'code' and module_name:
                    dic['module'] = module_name

                self._translate_dict.append(dic)

            # First process the entries from the PO file (doing so also fills/removes
            # the entries from the POT file).
            for row in reader:
                process_row(row)

            Translation.clear_caches()
            if verbose:
                _logger.info("translation file loaded successfully")

        except IOError:
            iso_lang = get_iso_codes(lang)
            filename = '[lang: %s][format: %s]' % (iso_lang or 'new', fileformat)
            _logger.exception("couldn't read translation file %s", filename)
