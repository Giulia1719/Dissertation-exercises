## Create a new section in your survey
To create a new section in your survey in OCTAVIUS, you will need to modify multiple files, which include:
1) XCS_WB\ui\src\Utils\helpers\format-name-of-survey-url.js
2) XCS_WB\ui\src\Utils\helpers\index.js
3) XCS_WB\ui\src\Routes\nameofsurvey\nameofsurvey-struct.js
4) XCS_WB\ui\src\Routes\nameofsurvey\nameofsurvey-components\image-manipulation-modal.jsx
5) XCS_WB\ui\src\Routes\nameofsurvey\nameofsurvey-components\image.jsx

First of all, create a new file in both XCS_WB\ui\src\Routes\nameofsurvey\nameofsurvey-components and XCS_WB\ui\src\Utils\helpers to store all the dynamical links for the different sections of the survey. I have called my file image-formatting.js. For example: 

``` 
export const formatSearchImageUrl = (datum, size, ext, index) =>
      `http://localhost:8000/OneDrive/Astrophysics_MPhys/Fourth_year/Dissertation/OCTAVIUS_GW/GWvetting_OCTAVIUS/${datum?.NAME}/srch_${index}.gif`;
```

In File 1, imports React and all the dynamic links functions from the local file previously created. The imported functions are used to create various image URLs based on the provided datum, size, and ext. Finally, export it so it can be imported and used in other files of your survey. An example is:

``` 
import React from 'react';
import { formatGWImageUrl, formatSearchImageUrl} from './image-formatting';

const FormatGwvettpracticeUrl = ({ datum, size, ext }) => {
  if (!datum) {
    console.log('No data available');
    return null;
  }

  const localImageUrl = formatGWImageUrl(datum, size, ext);
  const searchImageUrl = formatSearchImageUrl(datum, size, ext);

  console.log('localImageUrl:', localImageUrl);
  console.log('searchImageUrl:', searchImageUrl);
  
return(
<div className="image-urls">
      <div className="local-image" data-url={localImageUrl}></div>
      <div className="search-image" data-url={searchImageUrl}></div>
    </div>
  );
};

export default FormatGwvettpracticeUrl;
``` 

The terms "local-image" and "search-image" are the names you can choose yourself to assign to the dynamic link functions.

In File 2, you need to call the dynamic link functions you have created at the beginning. Leave all the other functions already called, if any: 

``` 
import { formatGWImageUrl, formatSearchImageUrl } from './image-formatting.js';
export {
  formatGWImageUrl,
  formatSearchImageUrl
};
```

In File 3, you need to physically add the section in the survey:

```
const GWVETTPRACTICETableStruct = {
  headers: {
  Object_image: {
      value: "Object_image",
      label: `Object_image`,
      sortable: false,
      desc: "Image of the object",
    },
  Search_images: {
      value: "Search_images",
      label: `Search_images`,
      sortable: false,
      desc: "Present images of the object",
    },
},
cells: {
  Object_image: props => <Image {...props} ext={'Object_image'} />,
  Search_images: props => <Image {...props} ext={'Search_images'} />,
},
```

In File 4, the module LazyLoadImage can be used to defers the loading of images until they are needed, to fasten image loading in the survey. For each new section, add after the TransforWrapper module:

```
<TransformWrapper
              onTransformed={(e) => handleTransform(e)}>
              <TransformComponent>
                <LazyLoadImage
                  src={formatGWImageUrl(datum, size, ext)} 
                  alt= "Object Image"
                  style={{
                    width: "798px",
                    height: "798px",
                    filter: `contrast(${manipulation.contrast}%) brightness(${manipulation.brightness}%) saturate(${manipulation.saturation}%)`
                  }}
                  effect="blur"
                  placeholderSrc="https://xcsresearchgroup.blob.core.windows.net/des-y6-images/DES_Y6_Images/28_DES_Y6_size_1x1-with_regions.png"
                />
               <LazyLoadImage
                  src={formatSearchImageUrl(datum,size,ext)}
                  alt= "Search Image"
                  style={{
                    width: "798px",
                    height: "798px",
                    filter: `contrast(${manipulation.contrast}%) brightness(${manipulation.brightness}%) saturate(${manipulation.saturation}%)`
                  }}
                  effect="blur"
                  placeholderSrc="https://xcsresearchgroup.blob.core.windows.net/des-y6-images/DES_Y6_Images/28_DES_Y6_size_1x1-with_regions.png"
                />
```

In File 5, import the file you have created at the beginning, togheter with any other module already imported, and call each dynamical link separately just for the relevant section in your survey. This avoids having the same image in 2 different sections:

```
import {formatGWImageUrl, formatSearchImageUrl} from './image-formatting';

if (ext === 'Object_image') {
  const imageUrl = formatGWImageUrl(datum, imageSize, ext);
  return (
    <LazyLoadImage
      className="LLI"
      style={{
        width: `${options?.imageVhHeight * 0.1}in`,
        height: `${options?.imageVhHeight * 0.1}in`,
      }}
      effect="blur"
      src={imageUrl}
      alt={`GW image for ${datum?.NAME || "Unnamed object"}`}
      placeholderSrc="https://xcsresearchgroup.blob.core.windows.net/gwvettpractice-images/GWVETTPRACTICE_Images/28_GWVETTPRACTICE_size_1x1-with_regions.png"
      onClick={handleModalToggle}
    />
  );
};
if (ext === 'Search_image') {
  const imageUrl = formatSearchImageUrl(datum, imageSize, ext);
  return (
    <LazyLoadImage
      className="LLI"
      style={{
        width: `${options?.imageVhHeight * 0.1}in`,
        height: `${options?.imageVhHeight * 0.1}in`,
      }}
      effect="blur"
      src={imageUrl}
      alt={`Search image for ${datum?.NAME || "Unnamed object"}`}
      placeholderSrc="https://xcsresearchgroup.blob.core.windows.net/gwvettpractice-images/GWVETTPRACTICE_Images/28_GWVETTPRACTICE_size_1x1-with_regions.png"
      onClick={handleModalToggle}
    />
  );
};
```
   
### Create a carousel section in your survey
If you want to create a carousel to display multiple images of the same object in the same section, you will need to create an additional file in XCS_WB\ui\src\Routes\nameofsurvey\nameofsurvey-components for it. An example of code is:

``` 
import React, { useState, useEffect } from 'react';
import { LazyLoadImage } from "react-lazy-load-image-component";
import { formatSearchImageUrl } from './image-formatting';

const loadImage = (url, retries = 3) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = resolve;
    img.onerror = () => {
      if (retries > 0) {
        setTimeout(() => loadImage(url, retries - 1).then(resolve).catch(reject), 1000);
      } else {
        reject();
      }
    };
    img.src = url;
  });
};

const SearchImageCarousel = ({ datum, options }) => {
  const [currentIndex, setCurrentIndex] = useState(1);
  const [maxIndex, setMaxIndex] = useState(1);
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    const findMaxIndex = async () => {
      let index = 1;
      while (true) {
        try {
          await loadImage(formatSearchImageUrl(datum, null, null, index));
          index++;
        } catch {
          break;
        }
      }
      setMaxIndex(index - 1);
      console.log(`Found ${index - 1} temp images for ${datum?.NAME}`);
    };

    findMaxIndex();
  }, [datum]);

  useEffect(() => {
    const loadCurrentImage = async () => {
      try {
        await loadImage(currentImageUrl);
        setImageError(false);
      } catch {
        console.error(`Failed to load image after retries: ${currentImageUrl}`);
        setImageError(true);
      }
    };

    loadCurrentImage();
  }, [currentIndex]);

  const nextImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex % maxIndex) + 1);
  };

  const prevImage = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 2 + maxIndex) % maxIndex + 1);
  };

  const currentImageUrl = formatSearchImageUrl(datum, null, null, currentIndex);

  console.log('Current image URL:', currentImageUrl);

  return (
    <div style={{ position: 'relative' }}>
      {imageError ? (
        <div>Error loading image</div>
      ) : (
        <LazyLoadImage
          className="LLI"
          style={{
            width: `${options?.imageVhHeight * 0.1}in`,
            height: `${options?.imageVhHeight * 0.1}in`,
          }}
          effect="blur"
          src={currentImageUrl}
          alt={`Search image ${currentIndex} for ${datum?.NAME || "Unnamed object"}`}
          placeholderSrc="https://xcsresearchgroup.blob.core.windows.net/gwvettpractice-images/GWVETTPRACTICE_Images/28_GWVETTPRACTICE_size_1x1-with_regions.png"
        />
      )}
      <button 
        onClick={prevImage} 
        style={{ position: 'absolute', left: 0, top: '50%', transform: 'translateY(-50%)' }}
      >
        &#8592;
      </button>
      <button 
        onClick={nextImage} 
        style={{ position: 'absolute', right: 0, top: '50%', transform: 'translateY(-50%)' }}
      >
        &#8594;
      </button>
    </div>
  );
};

export default SearchImageCarousel;
``` 

Hence, instead of writing the code that I have explained for File 5, you will just need to write:

``` 
if (ext === 'Search_images') {
  return <SearchImageCarousel datum={datum} options={options}/>;
}
```

with SearchImageCarousel the name of the file you have previously created. Remember to import the carousel file as you usually do for the dynamic link functions file. 
