
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import LandingPage from './pages/LandingPage';
import Login from './pages/auth/Login';
import Dashboard from './pages/admin/Dashboard';
import VehicleCosts from './pages/admin/VehicleCosts';
import RegisterVehicle from './pages/owner/RegisterVehicle';
import Register from './pages/renter/Register';
import VehicleListing from './pages/marketplace/VehicleListing';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route element={<PrivateRoute />}>
            <Route path="/admin/dashboard" element={<Dashboard />} />
            <Route path="/admin/vehicle-costs" element={<VehicleCosts />} />
            <Route path="/owner/register-vehicle" element={<RegisterVehicle />} />
            <Route path="/renter/register" element={<Register />} />
            <Route path="/marketplace" element={<VehicleListing />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
