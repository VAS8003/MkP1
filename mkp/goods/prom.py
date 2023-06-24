if __name__ == '__main__':
    import sys

    from django.core.management import execute_from_command_line

    if len(sys.argv) > 1 and sys.argv[1] == 'prom':
        # Код зчитування та оновлення файлу export.xlsx
        import pandas as pd
        from goods.models import Good

        df = pd.read_excel('export.xlsx')

        for index, row in df.iterrows():
            article = row['Код_товара']
            good = Good.objects.get(article=article)
            quantity = int(good.opt_stock)
            df.at[index, 'Количество'] = quantity

        df.to_excel('export.xlsx', index=False)
    else:
        execute_from_command_line(sys.argv)
