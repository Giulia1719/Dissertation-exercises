## Requirements for Survey Generator Script:
### Python requirements
 - `python 3.9+` (i think?)
 - `numpy`
 - `pandas`
 - `pymongo`

### Database account
 - Needs `DB_USERNAME` and `DB_PASSWORD` (might be able to use [api creds but not ideal?](../api/startup/mongoose.js))

### A survey you want to create
 - There is an example of a schema [here](https://github.com/TobyWallage/creating_test_survey)
    - Data should be a csv with the columns named as they will appear in ui
    - Reccomended to include a column `XCS_ID` that uniquely identify each object in your survey, if not provided will be auto generated however if you use this to identify your images no garentee it will match.
    - other stuff?

## How to use

Run this command to check usage of script
``` shell
python ./new_survey.py -h
```

Ensure your `DB_USERNAME` and `DB_PASSWORD` variables and set in your shell
e.g. <br/>
##### In bash
``` bash
export DB_USERNAME="your_username"
export DB_PASSWORD="your_password"
```
##### In powershell
``` powershell
$env:DB_USERNAME = "your_username"
$env:DB_PASSWORD = "your_password"
```

#### should be able to run command
``` shell
python ./new_survey.py -n testSurvey -c TEST_SURVEY -s /path/to/the/schema/for/survey/XAPA_schema.csv
```
Hopefully it works - if not check for any files it may of not cleaned up properly, common ones include `/XCS_WB/tmp/` and/or `/XCS_WB/ui/src/Routes/[nameOfYourSurvey]/`

Check it worked correctly starting a local app and navigating to
https://localhost:3000/xcs_portal/`YOUR_COLLECTION_CODE`

The table should contain the values from the schema you provided, however images will be default/nonexistent.

## Configuring Images

This requires a bit of modify javascript, currently a work in progress.

Find your newly created survey struct file in `./XCS_WB/ui/src/Routes/[nameOfYourSurvey]/[name-of-your-survey-struct.js` <br>
Example using the XAPA test survey: ![XAPA-test-strcut.js file](./docs/finding_struct_file.png)

Currently the struct will contain four default images for example shown below

![defaul images](./docs/default_images.png)

Unless you want these, they can be deleted/replaced with your own.
For example, in my XAPA_test_survey, I have;

![XAPA images example](./docs/XAPA_images_example.png)

Ensure;
- `value` matches the `key` (not strictly needed but helpful)
- `label` is what will be shown as column header
- `sortable` must be false
- `desc` is a short description shown when the user hovers their mouse over the `label`

*Lastly for this file*, near the bototm there will be the `cells` implementations of the values, again remove the default images values and replace with your own.
For the XAPA_test_survey example, I have commented out the defaults and added my own in form
``` jsx
value: props => <Image {...props} ext={"value"}>
```
where `value` matches the same `value`s used above! <br/><br/>
![Cells impl example](./docs/Cells_impl_example.png)

Finally *(hopefully)*, find the `format_url` file for your survey in `./XCW_WB/ui/src/Utils/helpers/format-[your-survey-name]-url.js`

``` js
const formatImageUrl = (datum, size, ext) =>
  `https://xcsresearchgroup.blob.core.windows.net/xapa-test-survey-images/XAPA_COMP_Images/${datum?.XCS_ID}_XAPA_COMP_ext_${ext}.png`;
```

Change the string formating to what your images would be called, note;
- `datum` is a struct containing the values for each row in the table, use it to acess the corresponding value from the schema you uploaded, for example the `XCS_ID` of the row.
- `size` is the current size selected by user from the dropdown, currently these are harded coded to defaults so can't really be modified easily.
- `ext` is the `value` from the table struct file that was modified previously, use this to know which image it should be. In my XAPA example I use it to distinguish between python images and IDL images

Once done, this url should be provided to Reese with the Images you want.<br/>
Additonally, this url can also be changed to external sources for example to get image directly from `legacy survey` *(although use sparingly since they will not like that)*.

