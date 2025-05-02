import axios from "axios";
import config from "../../config";

const apiURL = config.API_URL;
const api = axios.create({
  baseURL: apiURL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- USERS ---
export const getUsers = (params) => api.get("/users", { params });
export const getUserById = (id) => api.get(`/users/${id}`);
export const createUser = (data) => api.post("/users", data);
export const updateUserById = (id, data) => api.patch(`/users/${id}`, data);
export const deleteUserById = (id) => api.delete(`/users/${id}`);
export const bulkCreateUsers = (users) => api.post("/users/bulk", users);

// --- STUDENTS ---
export const getStudents = (params) => api.get("/students", { params });
export const getStudentById = (id) => api.get(`/students/${id}`);
export const createStudent = (data) => api.post("/students", data);
export const updateStudentById = (id, data) => api.patch(`/students/${id}`, data);
export const deleteStudentById = (id) => api.delete(`/students/${id}`);
export const bulkCreateStudents = (students) =>
  api.post("/students/bulk", students);

// --- LOGS ---
export const getLogs = (params) => api.get("/logs", { params });
export const getLogById = (id) => api.get(`/logs/${id}`);
export const createLog = (data) => api.post("/logs", data);
export const updateLogById = (id, data) => api.patch(`/logs/${id}`, data);
export const deleteLogById = (id) => api.delete(`/logs/${id}`);
export const bulkCreateLogs = (logs) => api.post("/logs/bulk", logs);

// --- TEACHERS ---
export const getTeachers = (params) => api.get("/teachers", { params });
export const getTeacherById = (id) => api.get(`/teachers/${id}`);
export const createTeacher = (data) => api.post("/teachers", data);
export const updateTeacherById = (id, data) => api.patch(`/teachers/${id}`, data);
export const deleteTeacherById = (id) => api.delete(`/teachers/${id}`);
export const bulkCreateTeachers = (teachers) =>
  api.post("/teachers/bulk", teachers);

// --- SUBJECTS ---
export const getSubjects = (params) => api.get("/subjects", { params });
export const getSubjectById = (id) => api.get(`/subjects/${id}`);
export const createSubject = (data) => api.post("/subjects", data);
export const updateSubjectById = (id, data) => api.patch(`/subjects/${id}`, data);
export const deleteSubjectById = (id) => api.delete(`/subjects/${id}`);
export const bulkCreateSubjects = (subjects) =>
  api.post("/subjects/bulk", subjects);
