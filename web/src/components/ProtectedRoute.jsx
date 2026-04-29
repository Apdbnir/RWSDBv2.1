import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = () => {
  const { isSuperUser, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading authentication...</div>; // Or a proper loading spinner
  }

  return isSuperUser ? <Outlet /> : <Navigate to="/" replace />;
};

export default ProtectedRoute;