import { useState, useEffect, useCallback } from 'react';
import {
  getUsers,
  getUserById,
  createUser,
  updateUserById,
  deleteUserById,
  bulkCreateUsers,
} from '../services/apiService';

// Получение всех пользователей
export function useUsers(params = {}) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getUsers(params);
      setUsers(res.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, loading, error, refetch: fetchUsers };
}

// Получение пользователя по ID
export function useUserById(id) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getUserById(id)
      .then((res) => setData(res.data))
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [id]);

  return { data, loading, error };
}

// Создание пользователя
export function useCreateUser() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const create = async (data) => {
    setLoading(true);
    try {
      const res = await createUser(data);
      return res.data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { create, loading, error };
}

// Обновление пользователя
export function useUpdateUserById() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null)

  const update = async (id, data) => {
    setLoading(true);
    try {
      const res = await updateUserById(id, data);
      console.log(res)
      if (res.status == 200) {
        setStatus('ok');
      }
      return res.data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }

  };

  return { update, loading, error, status };
}

// Удаление пользователя
export function useDeleteUserById() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const remove = async (id) => {
    setLoading(true);
    try {
      await deleteUserById(id);
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { remove, loading, error };
}

// Массовое создание
export function useBulkCreateUsers() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const bulkCreate = async (users) => {
    setLoading(true);
    try {
      const res = await bulkCreateUsers(users);
      return res.data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { bulkCreate, loading, error };
}
