import { createSlice } from '@reduxjs/toolkit';
import { findIdealNodeSearch } from '../../components/photo-gallery/utils/findIdealNodeSearch';
import { computeRowLayout } from '../../components/photo-gallery/layouts/justified';
import { computeColumnLayout } from '../../components/photo-gallery/layouts/columns';

export const photoSlice = createSlice({
  name: 'photos',
  initialState :{
    photos : [],
  },

  reducers: {
    setPhotos:(state, action) => {
      state.photos = [...state.photos, ...action.payload];
    },

    addPhotos:(state, action) => {
        state.photos = [...state.photos, ...action.payload];
    },
  },
 
});

export const { setPhotos, addPhotos, setContainerWidth, setData } = photoSlice.actions;
export const getPhotos = (state) => state.photos.photos;





export default photoSlice.reducer;