# -*- coding: utf-8 -*-

{
    "name": "ارسال پیامک ایران",
    "summary": "ارسال پیامک به واسطه وب سرویس sms.ir",
    "description": """
     ارسال پیامک
    
    برای تنظیم:
        * به بخش تنظیمات و منو تنظیمات عمومی مراجعه کنید 
        * تنظیمات آرتافرین را جستجو کنید.
        * اطلاعات خود را وارد کنید.
        * گزینه بازنویسی ارسال پیامک را فعال نمایید
    """,
    "version": "1.0",
    "depends": [
        'sms',
    ],
    "category": "Tools",
    "website": "https://www.fadoo.ir",
    "author": "saeed",
    "url": "https://www.fadoo.ir",
    "data": [
        'views/configuration.xml',
        'views/sms_sms.xml',
    ],
    "application": False,
    "installable": True,
    "active": True,
}
