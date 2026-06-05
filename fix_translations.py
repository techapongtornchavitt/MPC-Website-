import re, sys

path = r'C:\Users\Chavit\Downloads\brand guidlines mpc\lang.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def replace_in_block(text, block_start, block_end, updates):
    """Replace key values only within a specific range of the file."""
    segment = text[block_start:block_end]
    count = 0
    for key, new_val in updates.items():
        # Match: 'key-name'   :   'any existing value'  (handles ZWS, HTML, etc.)
        pattern = r"('" + re.escape(key) + r"'\s*:\s*')(?:[^'\\]|\\.)*'"
        escaped = new_val.replace('\\', '\\\\').replace("'", "\\'")
        new_seg, n = re.subn(pattern, r"\g<1>" + escaped + "'", segment)
        if n:
            segment = new_seg
            count += n
        else:
            print("  WARN: key not found in block: %s" % key)
    return text[:block_start] + segment + text[block_end:], count

# ── Find block boundaries ──────────────────────────────────────────────────
# Language blocks appear as "  th: {", "  km: {", etc.
th_pos  = content.index('\n    th:')
km_pos  = content.index('\n    km:')
lo_pos  = content.index('\n    lo:')
my_pos  = content.index('\n    mm:')
end_pos = len(content)

en_range  = (0,        th_pos)
th_range  = (th_pos,   km_pos)
km_range  = (km_pos,   lo_pos)
lo_range  = (lo_pos,   my_pos)
my_range  = (my_pos,   end_pos)

total = 0

# ══════════════════════════════════════════════════════════════════════════
# KM — Khmer updates
# ══════════════════════════════════════════════════════════════════════════
print("\nKM block")
km_updates = {
    'prod-tab-roller':    'ខ្សែសង្វាក់រំកិល',
    'prod-tab-conveyor':  'ខ្សែសង្វាក់បញ្ជូន',
    'prd-uno-desc':       'បានទទួលវិញ្ញាបនបត្រ ISO 9001 ។ ស៊េរី A &amp; B សសរថ្មមួយ និងច្រើន។ សន្សំចំណាយ ទន្ទឹមនឹងប្រសិទ្ធភាពខ្ពស់។',
    'prd-db-desc':        'ខ្សែសង្វាក់រំកិលស្តង់ដារ ANSI &mdash; សសរថ្មមួយ ពីរ &amp; បី។ ផលិតនៅប្រទេសកូរ៉េជាង ៤៥ ឆ្នាំ។',
    'prd-iwis-rl-desc':   'ខ្សែសង្វាក់រំកិលភាពជាក់លាក់អាល្លឺម៉ង់ &mdash; simplex &amp; duplex, ISO 606 បានធ្វើឱ្យប្រសើឡើងសម្រាប់ការដំណើរល្បឿនខ្ពស់ ដើម្បីកាត់បន្ថយសម្លេង។',
    'prd-sugar-desc':     'ខ្សែសង្វាក់ចម្លង គ្រឿងទន្ទឹម និងបញ្ជូនសម្រាប់ការផលិតស្ករ &mdash; ខ្សែ bagasse feeder, O-chain, bush chain និងបន្ថែមទៀត។',
    'bear-bc-active':     'បែរីង',
    'bear-h1':            '<em>បែរីង</em>',
    'bear-s1-h2':         'បែរីង',
    'bear-s2-intro':      'ជួររង្វង់បែរីងភាពជាក់លាក់ដ៏ទូលំទូលាយ សម្រាប់ប្រព័ន្ធដំណើរឧស្សាហកម្មគ្រប់ប្រភេទ។',
    'bear-s3-h2':         'ម៉ាកយីហោដែលយើងផ្តល់',
    'bear-s3-intro':      'យើងផ្គត់ផ្គង់បែរីងពិតប្រាកដពីក្រុមហ៊ុនផលិតឈានមុខគេលើពិភពលោក &mdash; ការតាមដានពេញលេញ គុណភាពបានបញ្ជាក់ មិនមានទំនិញក្លែងក្លាយ។',
    'bear-s4-h2':         'ភាពជាក់លាក់។ ការទុកចិត្ត។ ភាពគ្រប់ជ្រុងជ្រោយ។',
    'bear-s4-intro':      'ពីបែរីងតូចរហូតដល់គ្រឿងឧស្សាហកម្មធំ &mdash; យើងស្តុក និងទំនាក់ទំនងប្រភពតាមជួរពេញ។',
    'bear-iso-title':     'ផលិតផលពិតប្រាកដដែលមានការអនុញ្ញាត',
    'bear-iso-body':      'បែរីងទាំងអស់ដែលផ្គត់ផ្គង់ដោយ Motion Plus Corporation គឺជាផលិតផលពិតប្រាកដ ដែលទទួលបានពីបណ្តាញដែលមានការអនុញ្ញាតដោយផ្ទាល់ ។ ការតាមដានពេញលេញ គុណភាពបានបញ្ជាក់។',
    'bear-s1-p2':         'យើងស្តុក និងទំនាក់ទំនងប្រភពបែរីងពី SKF, FAG, TIMKEN, NTN, NSK, Koyo និងបន្ថែមទៀត &mdash; គ្របដណ្តប់ប្រភេទ Deep Groove Ball, Cylindrical Roller, Tapered Roller, Angular Contact និង Linear Bearing ។',
    'bear-step1-body':    'ប្រភេទបែរីងដែលប្រើប្រាស់ច្រើនជាងគេ &mdash; មាន open, shielded (ZZ) ឬ sealed (2RS) សម្រាប់ការប្រឆាំងការប្រឡាក់។',
    'bear-step2-body':    'សមត្ថភាពទទួលបន្ទុករ៉ាឌីយ៉ាលខ្ពស់ សម្រាប់ការប្រើប្រាស់ឧស្សាហកម្មធ្ងន់ធ្ងរ។ មានក្នុងការរៀបចំជួរតែមួយ និងច្រើនជួរ។',
    'bear-step3-body':    'ទទួលបន្ទុករ៉ាឌីយ៉ាល និងអ័ក្សសមូហភាព &mdash; ល្អសម្រាប់ប្រអប់លេខ ហ័រចក្ររថ និងម៉ាស៊ីនធ្ងន់ធ្ងរ។',
    'bear-step4-body':    'រ៉ែលណែនាំ THK និង NB linear, ball splines និង linear bushings សម្រាប់ការប្រើប្រាស់ចលនាលីនេអ៊ែរជាក់លាក់។',
    'bear-step5-body':    'Angular contact ball bearings សម្រាប់ spindle ល្បឿនខ្ពស់ និង spherical roller bearings សម្រាប់ការផ្តល់ misalignment compensation ។',
    'bear-step6-body':    'ការជ្រើសរើសបែរីងបច្ចេកទេស ការចង្អុលបង្ហាញឆ្លង និងការគាំទ្របន្ទាប់ការលក់ ពីក្រុមវិស្វករដែលមានបទពិសោធន៍របស់យើង។',
    'sp-bc-active':       'ស្ព្រូខេត &amp; រ៉ូលី',
    'sp-h1':              '<em>ស្ព្រូខេត</em> &amp; រ៉ូលី',
    'sp-overview-h2':     'ស្ព្រូខេត &amp; រ៉ូលី',
    'sp-cbadge1':         'ស្ព្រូខេតខ្សែសង្វាក់រំកិល',
    'sp-cbadge2':         'រ៉ូលី Timing',
    'sp-cbadge3':         'Taper Bore',
    'sp-cbadge4':         'ដែកអ៊ីណុក',
    'sp-cbadge5':         'Custom Bore',
    'sp-cbadge6':         'ច្រើនសសរថ្ម',
    'cpl-bc-active':      'គូប្លីង',
    'cpl-h1':             '<em>គូប្លីង</em>',
    'cpl-s1-h2':          'គូប្លីង',
    'os-bc-active':       'ទឹកប្រេងស៊ែល',
    'os-h1':              '<em>ទឹកប្រេងស៊ែល</em>',
    'os-s1-h2':           'ទឹកប្រេងស៊ែល',
    'belt-bc-active':     'ខ្សែក្រវ៉ាត់',
    'belt-h1':            '<em>ខ្សែក្រវ៉ាត់</em>',
    'belt-s1-h2':         'ខ្សែក្រវ៉ាត់',
    'belt-s2-h2':         'ម៉ាកយីហោខ្សែក្រវ៉ាត់ដែលយើងផ្តល់',
    'hs-cv-bc-active':    'ខ្សែសង្វាក់បញ្ជូន HS',
    'hs-cv-h1':           'ខ្សែសង្វាក់បញ្ជូន <em>HS</em>',
    'hs-cv-overview-h2':  'ខ្សែសង្វាក់បញ្ជូន HS',
    'hs-cv-cbadge2':      'បន្ទុកស្រាល',
    'hs-cv-cbadge3':      'បន្ទុកធ្ងន់',
    'hs-cv-step3-title':  'ការរចនាដែលមានប្រសិទ្ធភាព',
    'hs-cv-step4-title':  'ភាពចម្រុះឧស្សាហកម្ម',
    'cem-cbadge1':        'ខ្សែ Reclaimer',
    'cem-cbadge2':        'ខ្សែ Hoister',
    'cem-cbadge3':        'Apron Conveyor',
    'cem-ind-p1-h3':      'ខ្សែ Drag',
    'cem-ind-p2-h3':      'TRIO Clinker Drag Chain (P.102mm)',
    'iwis-step1-title':   'ការកែសម្រួលសម្លេង',
    'iwis-step4-title':   'អ្នកជំនាញដំណើរ Timing',
    'iwis-step5-title':   'សមត្ថភាពកាត់បន្ថយទំហំ',
    'iwis-step6-title':   'ការផលិតអាល្លឺម៉ង់',
    'iwis-cv-step2-title':'ឧបករណ៍បន្ថែមពិសេស',
    'iwis-cv-step4-title':'ការការពារច្រូតខ្យល់',
    'iwis-cv-step5-title':'ភាពជាក់លាក់នៃទំហំ',
    'soc-live-badge':     'ព័ត៌មានផ្ទាល់',
    'soc-stat-posts':     'ការបង្ហោះ',
    'soc-stat-followers': 'អ្នកតាម',
    'soc-stat-region':    'ការគ្របដណ្តប់',
    'soc-view-all':       'មើលការបង្ហោះទាំងអស់',
    'distrib-eyebrow':    'ផតហ្វូលីយ៉ូការចែកចាយ',
    'distrib-body':       'លើសពីម៉ាកយីហោដែលមានការអនុញ្ញាតទាំងបួនរបស់យើង MPC ចែកចាយផតហ្វូលីយ៉ូដ៏ទូលំទូលាយ នៃគ្រឿងឧបករណ៍ឧស្សាហកម្ម ពីក្រុមហ៊ុនផលិតឈានមុខគេពិភពលោក។',
    'hb-body':            'ខ្សែសង្វាក់ភាពជាក់លាក់ស្នាមមុខ MPC &mdash; រចនាឡើងសម្រាប់ការប្រើប្រាស់ demanding ទូទាំងអាស៊ីអាគ្នេយ៍។',
    'cont-form-lbl-company': 'ឈ្មោះក្រុមហ៊ុន',
    'cont-form-lbl-message':  'សារ',
    'cont-form-lbl-product':  'ផលិតផលដែលចាប់អារម្មណ៍',
    'sgm-step4-title':    'ការស្ថិតស្ថេរ &amp; ការហួតទឹក',
    'sgm-step5-title':    'ការស្ងួត &amp; ការច្រោះ',
    'sgm-step6-title':    'ខ្សែសាយការវេចខ្ចប់',
    'palm-s1-p1':         'ខ្សែសង្វាក់ប្រេងដូងត្រូវបានបង្កើតឡើងដោយផ្អែកលើការស្រាវជ្រាវ និងបទពិសោធន៍របស់យើងក្នុងឧស្សាហកម្មប្រេងដូង &mdash; វិស្វករកម្មសម្រាប់អាយុសេវាកម្មដ៏យូរ ក្រោមស្ថានភាពដែលមានការកិត និងបន្ទុកខ្ពស់។',
    'kmh-std-body':       'ប្រព័ន្ធបំពង់ conveyor ស្តង់ដារម៉ូឌុល &mdash; គ្រឿងបានរចនាជាមុន សម្រាប់ការតំឡើងលឿន និងការដោះស្រាយធូលី-ឥតទំ ជាប់ជាក់ ។',
    'kmh-spc-body':       'ដំណោះស្រាយបំពង់ conveyor ដែលបានរចនាខ្លួនឯងសម្រាប់ប្លង់រោងចក្រផ្ទាល់ &mdash; ការរចនាតាមបញ្ជា ការផលិតភាពជាក់លាក់។',
    'kmh-cat-btn':        'ទាញយក KMH Catalogue នៅទីនេះ',
}
content, n = replace_in_block(content, km_range[0], km_range[1], km_updates)
total += n
print("  %d replacements" % n)

# ══════════════════════════════════════════════════════════════════════════
# MY (Myanmar) updates
# ══════════════════════════════════════════════════════════════════════════
print("\n── MY block ──")
my_updates = {
    'prod-tab-roller':    'ရိုလာချိန်းများ',
    'prod-tab-conveyor':  'ကွန်ဗေယာချိန်းများ',
    'prod-tab-forged':    'ပုံသွင်းချိန်းများ',
    'prd-uno-name':       'UNO ချိန်းများ',
    'prd-uno-desc':       'ISO 9001 လက်မှတ်ရ။ A &amp; B စီးရီး၊ တစ်ချောင်းနှင့် ဘက်စုံကြင်။ ကုန်ကျစရိတ်သက်သာပြီး စွမ်းဆောင်ရည်မြင့်မားသည်။',
    'prd-db-name':        'Dongbo ချိန်းများ',
    'prd-db-desc':        'ANSI စံနှုန်းရိုလာချိန်းများ — တစ်ချောင်း၊ နှစ်ချောင်း &amp; သုံးချောင်းကြင်။ နှစ် ၄၅ ကျော် ကိုရီးယားထုတ်လုပ်မှု။',
    'prd-iwis-rl-name':   'IWIS ချိန်းများ',
    'prd-iwis-rl-desc':   'ဂျာမနီ တိကျမှုမြင့် ရိုလာချိန်းများ — simplex &amp; duplex၊ ISO 606၊ မြန်နှုန်းမြင့် မောင်းနှင်မှုအတွက် အသံနိမ့်အောင် ပြုလုပ်ထားသည်။',
    'prd-iwis-cv-name':   'IWIS ကွန်ဗေယာချိန်းများ',
    'prd-iwis-cv-desc':   'ရှုပ်ထွေးသော ကွန်ဗေယာစနစ်များအတွက် attachment၊ double-pitch၊ side-bow နှင့် hollow-pin မျိုးကွဲများ။',
    'prd-hs-cv-name':     'HS ကွန်ဗေယာချိန်းများ',
    'prd-hs-cv-desc':     'စက်မှုလုပ်ငန်းအမျိုးမျိုးတွင် ပစ္စည်းသယ်ယူပို့ဆောင်ရေးကို ချောမွေ့စေရန် အပေါ်စီးမှ လေးလံသောအလေးချိန်အထိ ကွန်ဗေယာချိန်းများ။',
    'prd-forged-name':    'ပုံသွင်းချိန်း TRIO / ပုံသွင်းချိန်း UNO',
    'prd-forged-desc':    'အရည်အသွေးမြင့် လေးလံသော ပုံသွင်းချိန်းများ — TRIO (P.102 mm) နှင့် UNO (P.142 mm) — သံမဏိစက်ရုံ၊ ဘိလပ်မြေစက်ရုံ &amp; တိရစ္ဆာန်အစာကြိတ်စက်ရုံများအတွက်။',
    'prd-sp-name':        'Sprocket များ &amp; Pulley များ',
    'prd-sp-desc':        'စံနှုန်း &amp; စိတ်ကြိုက်ပြုလုပ် sprocket နှင့် pulley များ — ရိုလာချိန်း sprocket များ၊ timing pulley များနှင့် လေးလံသောမောင်းနှင်မှုပစ္စည်းများ။',
    'prd-bearing-name':   'ဘဲယာ',
    'prd-bearing-desc':   'SKF, FAG, TIMKEN, NSK, NTN, Koyo &amp; အခြားများ — deep groove ball, cylindrical roller, tapered roller နှင့် linear ဘဲယာများ။',
    'prd-belt-name':      'ဘဲလ်',
    'prd-belt-desc':      'V-belt များ၊ Timing belt များ၊ Flat belt များနှင့် Synchronous belt များ။',
    'prd-coupling-name':  'ချိတ်ဆက်ကိရိယာ',
    'prd-coupling-desc':  'တိုင်ချိတ်ဆက်မှုဖြေရှင်းချက်များအတွက် jaw, flexible, chain နှင့် rigid coupling များ။',
    'prd-oilseal-name':   'ဆီတံဆိပ်',
    'prd-oilseal-desc':   'တောင်းဆိုမှုများသော အခြေအနေများတွင် ယုံကြည်စိတ်ချရသော တံဆိပ်ခတ်မှုအတွက် အလှည့်တိုင်နှင့် စက်မှုဆီတံဆိပ်များ။',
    'prd-pe1000-desc':    'High-density polyethylene ချောင်ချိပြားများ၊ လမ်းညွှန်ရေး rail များနှင့် စိတ်ကြိုက်ပြုလုပ် အစိတ်အပိုင်းများ။',
    'prd-kmhpipe-desc':   'KMH ပိုက်ပိတ်ကွန်ဗေယာစနစ်များ၊ လမ်းကြောင်းများနှင့် ဖုန်မကင်းသော အကြမ်းဖက်ပစ္စည်းသယ်ဆောင်ရေးအတွက် အစိတ်အပိုင်းများ။',
    'bear-bc-active':     'ဘဲယာ',
    'bear-h1':            '<em>ဘဲယာ</em>',
    'bear-s1-h2':         'ဘဲယာ',
    'bear-s1-p2':         'ကျွန်ုပ်တို့သည် SKF, FAG, TIMKEN, NTN, NSK, Koyo နှင့် အခြားများမှ ဘဲယာများကို သိုလှောင်ပြီး ရှာဖွေပေးသည် — deep groove ball, cylindrical roller, tapered roller, angular contact နှင့် linear ဘဲယာ အမျိုးအစားများ။',
    'bear-s2-intro':      'စက်မှုမောင်းနှင်မှုစနစ် တိုင်းအတွက် တိကျမှုမြင့် ဘဲယာများ၏ ကျယ်ပြန့်သောအကွာအဝေး။',
    'bear-s3-h2':         'ကျွန်ုပ်တို့ ကမ်းလှမ်းသော အမှတ်တံဆိပ်များ',
    'bear-s3-intro':      'ကျွန်ုပ်တို့သည် ကမ္ဘာ့ထိပ်တန်းထုတ်လုပ်သူများမှ စစ်မှန်သော ဘဲယာများကို ထောက်ပံ့ပေးသည် — ပြည့်စုံသောခြေရာခံနိုင်မှု၊ အသိအမှတ်ပြုအရည်အသွေး၊ အတုအပ မရှိ။',
    'bear-s4-h2':         'တိကျမှု။ ယုံကြည်စိတ်ချရမှု။ အကျုံးဝင်မှု။',
    'bear-s4-intro':      'သေးငယ်သောဘဲယာများမှ ကြီးမားသောစက်မှုယူနစ်များအထိ — ကျွန်ုပ်တို့သည် အပြည့်အဝ သိုလှောင်ပြီး ရှာဖွေပေးသည်။',
    'bear-iso-title':     'စစ်မှန်သော အတည်ပြုပေးထားသော ထုတ်ကုန်များ',
    'bear-iso-body':      'Motion Plus Corporation မှ ထောက်ပံ့သော ဘဲယာအားလုံးသည် တရားဝင်ချန်နယ်များမှ တိုက်ရိုက်ရယူသော စစ်မှန်သောထုတ်ကုန်များဖြစ်သည်။ ပြည့်စုံသောခြေရာခံနိုင်မှု၊ အသိအမှတ်ပြုအရည်အသွေး။',
    'bear-step1-title':   'Deep Groove Ball Bearings',
    'bear-step1-body':    'အသုံးအများဆုံး ဘဲယာအမျိုးအစား — open, shielded (ZZ) သို့မဟုတ် sealed (2RS) ရနိုင်သည်။',
    'bear-step2-title':   'Cylindrical Roller Bearings',
    'bear-step2-body':    'လေးလံသောစက်မှုလုပ်ငန်းသုံးများအတွက် မြင့်မားသော radial အလေးချိန်ဆောင်နိုင်မှုစွမ်းရည်။',
    'bear-step3-title':   'Tapered Roller Bearings',
    'bear-step3-body':    'radial နှင့် axial အလေးချိန်ပေါင်းစပ် ကိုင်တွယ်သည် — gear box များ၊ ဘီးဟပ်များနှင့် လေးလံသောစက်ပစ္စည်းများအတွက် အကောင်းဆုံး။',
    'bear-step4-title':   'Linear &amp; Motion Bearings',
    'bear-step4-body':    'တိကျသော linear လှုပ်ရှားမှုအတွက် THK နှင့် NB linear guide များ၊ ball spline များနှင့် linear bushing များ။',
    'bear-step5-title':   'Angular Contact &amp; Spherical',
    'bear-step5-body':    'မြန်နှုန်းမြင့် spindle အသုံးချမှုများအတွက် angular contact ball bearing များနှင့် မညီမညာမှုရောင်းလျော့ရေးအတွက် spherical roller bearing များ။',
    'bear-step6-title':   'နည်းပညာပံ့ပိုးမှု &amp; ရရှိနိုင်မှု',
    'bear-step6-body':    'ကျွန်ုပ်တို့၏ အင်ဂျင်နီယာအဖွဲ့မှ နည်းပညာဆိုင်ရာ ဘဲယာရွေးချယ်မှု၊ ကြိုးဝိုင်းညှိနှိုင်းမှုနှင့် အရောင်းနောက်ဆက်တွဲ ပံ့ပိုးမှု။',
    'bear-badge1':        'Deep Groove',
    'bear-cbadge1':       'Deep Groove Ball Bearing',
    'bear-cbadge2':       'Cylindrical Roller Bearing',
    'bear-cbadge3':       'Tapered Roller Bearing',
    'bear-cbadge4':       'Angular Contact',
    'bear-cbadge5':       'Spherical Roller',
    'bear-cbadge6':       'Linear Bearings',
    'sp-bc-active':       'Sprocket များ &amp; Pulley များ',
    'sp-h1':              '<em>Sprocket များ</em> &amp; Pulley များ',
    'sp-overview-h2':     'Sprocket များ &amp; Pulley များ',
    'sp-cbadge1':         'Roller Chain Sprockets',
    'sp-cbadge2':         'Timing Pulleys',
    'sp-cbadge3':         'Taper Bore',
    'sp-cbadge4':         'သံမဏိမကြေ',
    'sp-cbadge5':         'Custom Bore',
    'sp-cbadge6':         'Multi-Strand',
    'cpl-bc-active':      'ချိတ်ဆက်ကိရိယာ',
    'cpl-h1':             '<em>ချိတ်ဆက်ကိရိယာ</em>',
    'cpl-s1-h2':          'ချိတ်ဆက်ကိရိယာ',
    'os-bc-active':       'ဆီတံဆိပ်',
    'os-h1':              '<em>ဆီတံဆိပ်</em>',
    'os-s1-h2':           'ဆီတံဆိပ်',
    'belt-bc-active':     'ဘဲလ်',
    'belt-h1':            '<em>ဘဲလ်</em>',
    'belt-s1-h2':         'ဘဲလ်',
    'belt-s2-h2':         'ကျွန်ုပ်တို့ ကမ်းလှမ်းသော ဘဲလ်အမှတ်တံဆိပ်များ',
    'hs-cv-bc-active':    'HS ကွန်ဗေယာချိန်းများ',
    'hs-cv-h1':           '<em>HS</em> ကွန်ဗေယာချိန်းများ',
    'hs-cv-overview-h2':  'HS ကွန်ဗေယာချိန်းများ',
    'hs-cv-cbadge2':      'အပေါ်စီးအလေးချိန်',
    'hs-cv-cbadge3':      'လေးလံသောအလေးချိန်',
    'hs-cv-step3-title':  'စွမ်းဆောင်ရည်မြင့် ဒီဇိုင်း',
    'hs-cv-step4-title':  'စက်မှုလုပ်ငန်းအမျိုးမျိုးအတွက် သင့်တော်မှု',
    'cem-cbadge1':        'Reclaimer ချိန်း',
    'cem-cbadge2':        'Hoister ချိန်း',
    'cem-cbadge3':        'Apron ကွန်ဗေယာ',
    'cem-ind-p1-h3':      'Drag ချိန်း',
    'cem-ind-p2-h3':      'TRIO Clinker Drag ချိန်း (P.102mm)',
    'cem-ind-ovr-eyebrow':'ဘိလပ်မြေစက်ရုံ အင်ဂျင်နီယာကျွမ်းကျင်သူများ',
    'cem-step1-title':    'Reclaimer ချိန်း',
    'cem-step2-title':    'Hoister ချိန်း',
    'cem-step3-title':    'Apron ကွန်ဗေယာချိန်း',
    'cem-step4-title':    'Slide Fastener စက်ချိန်း',
    'sgm-step1-title':    'ကုန်ကြမ်းပစ္စည်းကိုင်တွယ်မှု',
    'sgm-step2-title':    'သကြားရည်ညှစ်ထုတ်ခြင်းလုပ်ငန်းစဉ်',
    'sgm-step3-title':    'ကြံဖြတ်သန်းကျန်သယ်ဆောင်ခြင်း',
    'sgm-step4-title':    'အနှစ်ချပြီး အငွေ့ပျံစေခြင်း',
    'sgm-step5-title':    'အခြောက်ခံခြင်း &amp; စစ်ထုတ်ခြင်း',
    'sgm-step6-title':    'ထုပ်ပိုးစောင်းတန်း',
    'iwis-step1-title':   'အသံပြဿနာဖြေရှင်းချုပ်ညှိမှု',
    'iwis-step4-title':   'Timing Drive ကျွမ်းကျင်သူ',
    'iwis-step5-title':   'အရွယ်အစားလျှော့ချနိုင်မှု',
    'iwis-step6-title':   'ဂျာမနီထုတ်လုပ်မှု',
    'iwis-cv-step2-title':'အထူးချိတ်တွဲများ',
    'iwis-cv-step4-title':'သံချေးတားဆီးကာကွယ်မှု',
    'iwis-cv-step5-title':'အတိုင်းအတာ တိကျမှု',
    'soc-live-badge':     'တိုက်ရိုက်ဖော်ပြချက်',
    'soc-stat-posts':     'ပို့စ်များ',
    'soc-stat-followers': 'နောက်လိုက်များ',
    'soc-stat-region':    'အကျုံးဝင်ဒေသ',
    'soc-view-all':       'ပို့စ်အားလုံးကြည့်ရန်',
    'cont-form-h2':       'စုံစမ်းမေးမြန်းရေးဖောင်',
    'cont-form-lbl-company':  'ကုမ္ပဏီအမည်',
    'cont-form-lbl-message':  'မက်ဆေ့ချ်',
    'cont-form-lbl-product':  'စိတ်ဝင်စားသောထုတ်ကုန်',
    'distrib-eyebrow':    'ဖြန့်ဖြူးရေး ပေါ်တဖိုလီယို',
    'distrib-body':       'တရားဝင်အမှတ်တံဆိပ်လေးခုအပြင်၊ MPC သည် ကမ္ဘာ့ထိပ်တန်းထုတ်လုပ်သူများမှ စက်မှုအစိတ်အပိုင်းများ၏ ကျယ်ပြန့်သောပေါ်တဖိုလီယိုကို ဖြန့်ဖြူးသည်။',
    'hb-body':            'အရှေ့တောင်အာရှတစ်ဝှမ်း တောင်းဆိုမှုများသောအသုံးချမှုများအတွက် ဒီဇိုင်းထုတ်ထားသော MPC အရည်အသွေးတံဆိပ်တပ်ဆင် တိကျစွာ ပုံသွင်းထားသောချိန်းများ။',
}
content, n = replace_in_block(content, my_range[0], my_range[1], my_updates)
total += n
print("  %d replacements" % n)

# ══════════════════════════════════════════════════════════════════════════
# LO — Lao updates
# ══════════════════════════════════════════════════════════════════════════
print("\n── LO block ──")
lo_updates = {
    'bear-badge1':        'Deep Groove',
    'bear-cbadge1':       'Deep Groove Ball Bearing',
    'bear-cbadge2':       'Cylindrical Roller Bearing',
    'bear-cbadge3':       'Tapered Roller Bearing',
    'bear-cbadge4':       'Angular Contact',
    'bear-cbadge5':       'Spherical Roller',
    'bear-cbadge6':       'Linear Bearings',
    'bear-step1-title':   'Deep Groove Ball Bearings',
    'bear-step2-title':   'Cylindrical Roller Bearings',
    'bear-step3-title':   'Tapered Roller Bearings',
    'bear-step4-title':   'Linear &amp; Motion Bearings',
    'bear-step5-title':   'Angular Contact &amp; Spherical',
    'sp-cbadge3':         'Taper Bore',
    'sp-cbadge4':         'ສະແຕນເລດ',
    'sp-cbadge5':         'Custom Bore',
    'sp-cbadge6':         'ຫຼາຍສາຍ',
    'cem-step1-title':    'ລະບົບໂສ້ Reclaimer',
    'cem-step2-title':    'ລະບົບໂສ້ Hoister',
    'cem-step3-title':    'ໂສ້ສາຍພານ Apron Conveyor',
    'cem-step4-title':    'ໂສ້ເຄື່ອງ Slide Fastener',
    'cem-cbadge1':        'Reclaimer Chain',
    'cem-cbadge2':        'Hoister Chain',
    'cem-cbadge3':        'Apron Conveyor',
    'cem-ind-p1-h3':      'Drag Chain',
    'cem-ind-p2-h3':      'TRIO Clinker Drag Chain (P.102mm)',
    'sgm-step4-title':    'ການຕົກຕະກອນ &amp; ການລະເຫີຍ',
    'sgm-step5-title':    'ການອົບແຫ້ງ &amp; ການຄັດກອງ',
    'sgm-step6-title':    'ສາຍການຫຸ້ມຫໍ່',
    'iwis-step1-title':   'ການເພີ່ມປະສິດທິພາບສຽງ',
    'iwis-step4-title':   'ຜູ້ຊ່ຽວຊານດ້ານ Timing Drive',
    'iwis-step5-title':   'ຄວາມສາມາດໃນການຫຼຸດຂະໜາດ',
    'iwis-cv-step5-title':'ຄວາມຖືກຕ້ອງຂອງຂະໜາດ',
    'hs-cv-cbadge2':      'ຮັບນ້ຳໜັກເບົາ',
    'hs-cv-cbadge3':      'ຮັບນ້ຳໜັກໜັກ',
    'hs-cv-step3-title':  'ການອອກແບບທີ່ຂັບເຄື່ອນດ້ວຍປະສິດທິພາບ',
    'hs-cv-step4-title':  'ຄວາມຫຼາກຫຼາຍໃນຫຼາຍອຸດສາຫະກໍາ',
    'soc-live-badge':     'ຟີດສົດ',
    'soc-stat-posts':     'ໂພດ',
    'soc-stat-followers': 'ຜູ້ຕິດຕາມ',
    'soc-stat-region':    'ການຄຸ້ມຄອງ',
    'soc-view-all':       'ເບິ່ງທຸກໂພດ',
}
content, n = replace_in_block(content, lo_range[0], lo_range[1], lo_updates)
total += n
print("  %d replacements" % n)

# ══════════════════════════════════════════════════════════════════════════
# TH — Thai updates (bearing badge/step labels only)
# ══════════════════════════════════════════════════════════════════════════
print("\n── TH block ──")
th_updates = {
    'bear-cbadge1':       'ตลับลูกปืนร่องลึก',
    'bear-cbadge2':       'ตลับลูกปืนลูกกลิ้งทรงกระบอก',
    'bear-cbadge3':       'ตลับลูกปืนลูกกลิ้งเรียว',
    'bear-cbadge4':       'Angular Contact',
    'bear-cbadge5':       'Spherical Roller',
    'bear-cbadge6':       'Linear Bearings',
    'bear-step1-title':   'ตลับลูกปืนร่องลึก (Deep Groove Ball Bearings)',
    'bear-step2-title':   'ตลับลูกปืนลูกกลิ้งทรงกระบอก (Cylindrical Roller Bearings)',
    'bear-step3-title':   'ตลับลูกปืนลูกกลิ้งเรียว (Tapered Roller Bearings)',
    'bear-step4-title':   'ตลับลูกปืนเชิงเส้น &amp; Motion Bearings',
    'bear-step5-title':   'Angular Contact &amp; Spherical',
    'sp-cbadge3':         'Taper Bore',
    'sp-cbadge4':         'สแตนเลส',
    'sp-cbadge5':         'Custom Bore',
    'sp-cbadge6':         'หลายสาย',
}
content, n = replace_in_block(content, th_range[0], th_range[1], th_updates)
total += n
print("  %d replacements" % n)

# ── Write result ───────────────────────────────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nTotal replacements: %d" % total)
print("Done.")
