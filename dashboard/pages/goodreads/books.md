# Books

```sql summary
select
    count(*) filter (shelf = 'read') as total_read,
    count(*) filter (shelf = 'currently-reading') as reading,
    count(*) filter (shelf = 'to-read') as to_read,
    round(avg(user_rating) filter (user_rating is not null), 2) as avg_rating,
    sum(num_pages) filter (shelf = 'read' and num_pages is not null) as total_pages_read
from personal_data.goodreads_books
```

```sql read_by_year
select
    year_read::integer as year,
    count(*) as books_read
from personal_data.goodreads_books
where shelf = 'read' and year_read is not null
group by year_read
order by year_read
```

```sql top_rated
select
    title,
    author,
    user_rating,
    avg_rating,
    num_pages,
    date_read
from personal_data.goodreads_books
where shelf = 'read' and user_rating is not null
order by user_rating desc, avg_rating desc
limit 25
```

```sql currently_reading
select title, author, num_pages, date_added
from personal_data.goodreads_books
where shelf = 'currently-reading'
```

```sql to_read
select title, author, num_pages, avg_rating, date_added
from personal_data.goodreads_books
where shelf = 'to-read'
order by avg_rating desc
```

<BigValue data={summary} value="total_read" title="Books Read" />
<BigValue data={summary} value="reading" title="Currently Reading" />
<BigValue data={summary} value="to_read" title="To Read" />
<BigValue data={summary} value="avg_rating" title="Avg Rating" fmt="num2" />
<BigValue data={summary} value="total_pages_read" title="Pages Read" fmt="num0" />

### Books Read by Year

<BarChart data={read_by_year} x=year y=books_read yAxisTitle="Books" />

### Top Rated

<DataTable data={top_rated} rows=25 />

### Currently Reading

<DataTable data={currently_reading} />

### To Read

<DataTable data={to_read} />
