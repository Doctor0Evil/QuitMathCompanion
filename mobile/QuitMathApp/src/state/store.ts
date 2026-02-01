import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import cravingsReducer from "./cravingsSlice";
import tasksReducer from "./tasksSlice";
import sessionsReducer from "./sessionsSlice";
import ecoReducer from "./ecoSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cravings: cravingsReducer,
    tasks: tasksReducer,
    sessions: sessionsReducer,
    eco: ecoReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
