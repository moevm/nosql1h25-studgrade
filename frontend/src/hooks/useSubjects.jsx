import { useState, useEffect, useCallback } from "react";
import {
  getSubjects,
  getSubjectById,
  createSubject,
  updateSubjectById,
  deleteSubjectById,
  bulkCreateSubjects,
} from "../services/apiService";

export function useSubjects(params = {}) {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSubjects = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getSubjects(params);
      setSubjects(res.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchSubjects();
  }, [fetchSubjects]);

  return { subjects, loading, error, refetch: fetchSubjects };
}

export function useSubjectById(id) {
  const [subject, setSubject] = useState(null);
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getSubjectById(id)
      .then((res) => setSubject(res.data))
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [id]);

  return { subject, loading, error };
}

export function useCreateSubject() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const create = async (data) => {
    setLoading(true);
    try {
      const res = await createSubject(data);
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

export function useUpdateSubjectById() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const update = async (id, data) => {
    setLoading(true);
    try {
      const res = await updateSubjectById(id, data);
      return res.data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { update, loading, error };
}

export function useDeleteSubjectById() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const remove = async (id) => {
    setLoading(true);
    try {
      await deleteSubjectById(id);
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { remove, loading, error };
}

export function useBulkCreateSubjects() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const bulkCreate = async (subjects) => {
    setLoading(true);
    try {
      const res = await bulkCreateSubjects(subjects);
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
