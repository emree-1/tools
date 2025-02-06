# KeyFind

| Option name          | Usage                     | Description                                                            |
| -------------------- | ------------------------- | ---------------------------------------------------------------------- |
| **Keywords**         | `-k [KEYS]`               | Define the list of keywords to search for.                             |
| **Variants formats** | `-v [VARIANTS]`           | Specify the types of variants to generate for each keyword.            |
| **Render format**    | `-r [FORMAT]`             | Specify the output format for rendering the results.                   |
| **Extract file**     | `-e [OUTFILE]`            | Output filename to save the extracted results.                         |
| **Parameters**       | `-p [PARAMETERS]`         | Define an alternate table format for output.                           |
| **Order**            | `-o [ORDER]`              | Specify parameter to order result.                                     |
| **Invert order**     | `--inv_order`             | Invert the ordering of the results.                                    |
| **Caesar shift**     | `--caesar_shift [SHIFTS]` | Define the shifts to apply for generating Caesar cipher variants.      |
| **Table format**     | `--tblfmt [FORMAT]`       | Specify an other table format for the output.                          |
| **Minimum count**    | `--min [MIN]`             | Set the minimum count threshold for a result to be included.           |
| **Maximum count**    | `--max [MAX]`             | Set the maximum count threshold for a result to be included.           |
| **Remove duplicate** | `--remove_duplicate`      | Remove duplicate results from the output.                              |
| **Case sensitive**   | `--case_sensitive`        | Enables case-sensitive keyword matching (not yet implemented).         |
| **Index**            | `--index`                 | Add an index when extracting results.                                  |
| **Hide zero**        | `--hide_zero`             | Hide results where no matches are found for a keyword or its variants. |
| **No plain**         | `--no_plain`              | Excludes plain keywords defined by the user from being searched.       |
| **No space**         | `--no_space`              | Trims leading and trailing spaces from the results before printing.    |
| **No summary**       | `--no_summary`            | Disable the display of a results summary.                              |
| **Verbose**          | `--verbose`               | Enable verbose mode for detailed output.                               |
| **Quiet**            | `--quiet`                 | Suppresses output, except for critical information.                    |
| **Very Quiet**       | `--qquiet`                | Suppresses all output, including banners and other messages.           |
| **Time**             | `--time`                  | Displays the execution time of the script after completion.            |