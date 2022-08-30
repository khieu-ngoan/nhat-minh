import { configureStore } from '@reduxjs/toolkit';
import phothoReducer from './gallery/photoSlice';

export default configureStore({
  reducer: {
    photos: phothoReducer,
  },
});
