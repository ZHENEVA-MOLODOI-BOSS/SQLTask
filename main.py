# SQL блок.
# В онлайн торгах участвуют несколько товаров, для них каждый день по закрытию торгов записывается последняя цена.
# Для каждого из товаров необходимо найти количество дней, за которое цена на него устоялась
# (устоявшейся ценой считаем ту, после которой от дня к дню цена менялась не более чем на 3%).
# В качестве результата необходимо получить таблицу [product_name, days_num].
# Если такой даты нет, необходимо вывести -1.


CREATE TABLE hive.default.online_trade_table (
	product_name varchar,
	report_date date,
	day_price int
);

select product_name, case when SUM(diff_price_flag)> 0 then SUM(diff_price_flag) else -1 end days_num
from (select product_name,
        day_price,
          report_date,
          yesterdays_price,
        case when (((day_price - yesterdays_price) * 100) / day_price) <= 3 then 1 else 0 end diff_price_flag
      from (select product_name,
              day_price,
              report_date,
              LAG(day_price) over (partition by product_name order by report_date asc) as yesterdays_price
              from default.online_trade_table
          ) tb1
      ) tb2
group by product_name;

