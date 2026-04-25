import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { User, UserRole } from '../../types';

// ─── Types ────────────────────────────────────────────────────────────────────

interface UserFormData {
  full_name: string;
  email: string;
  password: string;
  role: UserRole;
  is_active: boolean;
}

interface Toast {
  id: number;
  type: 'success' | 'error';
  message: string;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const ROLE_LABELS: Record<UserRole, string> = {
  ADMIN: 'Administrador',
  OWNER: 'Proprietário',
  RENTER: 'Locatário',
};

const ROLE_COLORS: Record<UserRole, string> = {
  ADMIN: 'bg-purple-100 text-purple-800',
  OWNER: 'bg-blue-100 text-blue-800',
  RENTER: 'bg-green-100 text-green-800',
};

const EMPTY_FORM: UserFormData = {
  full_name: '',
  email: '',
  password: '',
  role: 'RENTER',
  is_active: true,
};

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short' }).format(new Date(iso));
}

// ─── Sub-components ───────────────────────────────────────────────────────────

const RoleBadge: React.FC<{ role: UserRole }> = ({ role }) => (
  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${ROLE_COLORS[role]}`}>
    {ROLE_LABELS[role]}
  </span>
);

const StatusBadge: React.FC<{ active: boolean }> = ({ active }) => (
  <span
    className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
      active ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-700'
    }`}
  >
    <span className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-emerald-500' : 'bg-red-500'}`} />
    {active ? 'Ativo' : 'Inativo'}
  </span>
);

// ─── Main Component ───────────────────────────────────────────────────────────

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState<UserRole | ''>('');
  const [toasts, setToasts] = useState<Toast[]>([]);
  const toastCounter = useRef(0);

  // Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editUser, setEditUser] = useState<User | null>(null);
  const [passwordUser, setPasswordUser] = useState<User | null>(null);
  const [deleteUser, setDeleteUser] = useState<User | null>(null);

  // Form state
  const [form, setForm] = useState<UserFormData>(EMPTY_FORM);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // ── Toast helpers ────────────────────────────────────────────────────────

  const addToast = useCallback((type: 'success' | 'error', message: string) => {
    const id = ++toastCounter.current;
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 4000);
  }, []);

  // ── Data loading ─────────────────────────────────────────────────────────

  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<User[]>('/users');
      setUsers(res.data);
    } catch {
      addToast('error', 'Falha ao carregar usuários.');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  // ── Derived list ─────────────────────────────────────────────────────────

  const filtered = users.filter((u) => {
    const q = search.toLowerCase();
    const matchesSearch =
      !q || u.full_name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q);
    const matchesRole = !roleFilter || u.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  // ── Create ───────────────────────────────────────────────────────────────

  const openCreate = () => {
    setForm(EMPTY_FORM);
    setShowCreateModal(true);
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post('/users', form);
      addToast('success', 'Usuário criado com sucesso!');
      setShowCreateModal(false);
      loadUsers();
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      addToast('error', detail ?? 'Erro ao criar usuário.');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Edit ─────────────────────────────────────────────────────────────────

  const openEdit = (user: User) => {
    setForm({
      full_name: user.full_name,
      email: user.email,
      password: '',
      role: user.role,
      is_active: user.is_active,
    });
    setEditUser(user);
  };

  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editUser) return;
    setSubmitting(true);
    try {
      await api.put(`/users/${editUser.id}`, {
        full_name: form.full_name,
        role: form.role,
        is_active: form.is_active,
      });
      addToast('success', 'Usuário atualizado com sucesso!');
      setEditUser(null);
      loadUsers();
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      addToast('error', detail ?? 'Erro ao atualizar usuário.');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Change password ──────────────────────────────────────────────────────

  const openChangePassword = (user: User) => {
    setNewPassword('');
    setConfirmPassword('');
    setPasswordUser(user);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!passwordUser) return;
    if (newPassword !== confirmPassword) {
      addToast('error', 'As senhas não coincidem.');
      return;
    }
    if (newPassword.length < 8) {
      addToast('error', 'A senha deve ter no mínimo 8 caracteres.');
      return;
    }
    setSubmitting(true);
    try {
      await api.put(`/users/${passwordUser.id}/password`, { new_password: newPassword });
      addToast('success', 'Senha alterada com sucesso!');
      setPasswordUser(null);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      addToast('error', detail ?? 'Erro ao alterar senha.');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Delete ───────────────────────────────────────────────────────────────

  const handleDelete = async () => {
    if (!deleteUser) return;
    setSubmitting(true);
    try {
      await api.delete(`/users/${deleteUser.id}`);
      addToast('success', 'Usuário removido com sucesso!');
      setDeleteUser(null);
      loadUsers();
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      addToast('error', detail ?? 'Erro ao remover usuário.');
    } finally {
      setSubmitting(false);
    }
  };

  // ─────────────────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ── Toast Stack ──────────────────────────────────────────────────── */}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`animate-fadeIn flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-sm font-medium text-white max-w-xs ${
              t.type === 'success' ? 'bg-emerald-600' : 'bg-red-600'
            }`}
          >
            <i className={`fa-solid ${t.type === 'success' ? 'fa-circle-check' : 'fa-circle-xmark'}`} />
            {t.message}
          </div>
        ))}
      </div>

      {/* ── Header ───────────────────────────────────────────────────────── */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/admin/dashboard" className="text-gray-400 hover:text-gray-600 transition">
            <i className="fa-solid fa-arrow-left" />
          </Link>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Gerenciamento de Usuários</h1>
            <p className="text-xs text-gray-500 mt-0.5">Administre contas, papéis e senhas</p>
          </div>
        </div>
        <button
          onClick={openCreate}
          className="flex items-center gap-2 bg-navy text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-gray-800 transition shadow"
        >
          <i className="fa-solid fa-plus" />
          Novo Usuário
        </button>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
        {/* ── Stats ──────────────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
          {[
            { label: 'Total', count: users.length, icon: 'fa-users', color: 'text-navy' },
            { label: 'Admins', count: users.filter((u) => u.role === 'ADMIN').length, icon: 'fa-shield-halved', color: 'text-purple-600' },
            { label: 'Proprietários', count: users.filter((u) => u.role === 'OWNER').length, icon: 'fa-car', color: 'text-blue-600' },
            { label: 'Locatários', count: users.filter((u) => u.role === 'RENTER').length, icon: 'fa-id-card', color: 'text-green-600' },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 flex items-center gap-3">
              <div className={`w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 ${s.color}`}>
                <i className={`fa-solid ${s.icon} text-lg`} />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{s.count}</p>
                <p className="text-xs text-gray-500">{s.label}</p>
              </div>
            </div>
          ))}
        </div>

        {/* ── Filters ────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 mb-5 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <i className="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm" />
            <input
              type="text"
              placeholder="Buscar por nome ou e-mail…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-navy focus:border-transparent"
            />
          </div>
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value as UserRole | '')}
            className="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-navy focus:border-transparent bg-white"
          >
            <option value="">Todos os papéis</option>
            <option value="ADMIN">Administrador</option>
            <option value="OWNER">Proprietário</option>
            <option value="RENTER">Locatário</option>
          </select>
          {(search || roleFilter) && (
            <button
              onClick={() => { setSearch(''); setRoleFilter(''); }}
              className="text-sm text-gray-500 hover:text-gray-800 flex items-center gap-1 transition"
            >
              <i className="fa-solid fa-xmark" /> Limpar
            </button>
          )}
        </div>

        {/* ── Table ──────────────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 text-gray-400">
              <i className="fa-solid fa-circle-notch fa-spin text-3xl mb-3" />
              <p className="text-sm">Carregando usuários…</p>
            </div>
          ) : filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-gray-400">
              <i className="fa-solid fa-users-slash text-3xl mb-3" />
              <p className="text-sm font-medium">Nenhum usuário encontrado</p>
              <p className="text-xs mt-1">Tente ajustar os filtros ou adicione um novo usuário.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-100">
                    <th className="text-left px-5 py-3 font-semibold text-gray-500 text-xs uppercase tracking-wide">
                      Usuário
                    </th>
                    <th className="text-left px-5 py-3 font-semibold text-gray-500 text-xs uppercase tracking-wide hidden sm:table-cell">
                      Papel
                    </th>
                    <th className="text-left px-5 py-3 font-semibold text-gray-500 text-xs uppercase tracking-wide hidden md:table-cell">
                      Status
                    </th>
                    <th className="text-left px-5 py-3 font-semibold text-gray-500 text-xs uppercase tracking-wide hidden lg:table-cell">
                      Criado em
                    </th>
                    <th className="text-right px-5 py-3 font-semibold text-gray-500 text-xs uppercase tracking-wide">
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {filtered.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-50/60 transition-colors group">
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-full bg-navy/10 flex items-center justify-center flex-shrink-0">
                            <span className="text-navy font-bold text-sm">
                              {user.full_name.charAt(0).toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <p className="font-semibold text-gray-900">{user.full_name}</p>
                            <p className="text-gray-500 text-xs">{user.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-5 py-3.5 hidden sm:table-cell">
                        <RoleBadge role={user.role} />
                      </td>
                      <td className="px-5 py-3.5 hidden md:table-cell">
                        <StatusBadge active={user.is_active} />
                      </td>
                      <td className="px-5 py-3.5 text-gray-500 hidden lg:table-cell">
                        {formatDate(user.created_at)}
                      </td>
                      <td className="px-5 py-3.5">
                        <div className="flex items-center justify-end gap-1">
                          <ActionButton
                            title="Editar usuário"
                            icon="fa-pen"
                            color="hover:bg-blue-50 hover:text-blue-600"
                            onClick={() => openEdit(user)}
                          />
                          <ActionButton
                            title="Alterar senha"
                            icon="fa-key"
                            color="hover:bg-amber-50 hover:text-amber-600"
                            onClick={() => openChangePassword(user)}
                          />
                          <ActionButton
                            title="Remover usuário"
                            icon="fa-trash"
                            color="hover:bg-red-50 hover:text-red-600"
                            onClick={() => setDeleteUser(user)}
                          />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {!loading && filtered.length > 0 && (
            <div className="px-5 py-3 border-t border-gray-100 text-xs text-gray-400">
              {filtered.length} {filtered.length === 1 ? 'usuário' : 'usuários'} encontrado{filtered.length !== 1 ? 's' : ''}
              {users.length !== filtered.length && ` (de ${users.length} no total)`}
            </div>
          )}
        </div>
      </div>

      {/* ── Create Modal ─────────────────────────────────────────────────── */}
      {showCreateModal && (
        <Modal title="Novo Usuário" onClose={() => setShowCreateModal(false)}>
          <form onSubmit={handleCreate} className="space-y-4">
            <Field label="Nome completo">
              <input
                type="text"
                required
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                className={inputCls}
                placeholder="João Silva"
              />
            </Field>
            <Field label="E-mail">
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className={inputCls}
                placeholder="joao@exemplo.com"
              />
            </Field>
            <Field label="Senha">
              <input
                type="password"
                required
                minLength={8}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className={inputCls}
                placeholder="Mínimo 8 caracteres"
              />
            </Field>
            <Field label="Papel">
              <RoleSelect value={form.role} onChange={(r) => setForm({ ...form, role: r })} />
            </Field>
            <Field label="Status">
              <ActiveToggle value={form.is_active} onChange={(v) => setForm({ ...form, is_active: v })} />
            </Field>
            <ModalFooter onCancel={() => setShowCreateModal(false)} submitting={submitting} label="Criar Usuário" />
          </form>
        </Modal>
      )}

      {/* ── Edit Modal ───────────────────────────────────────────────────── */}
      {editUser && (
        <Modal title="Editar Usuário" onClose={() => setEditUser(null)}>
          <div className="flex items-center gap-3 mb-5 p-3 bg-gray-50 rounded-xl">
            <div className="w-10 h-10 rounded-full bg-navy/10 flex items-center justify-center flex-shrink-0">
              <span className="text-navy font-bold">{editUser.full_name.charAt(0).toUpperCase()}</span>
            </div>
            <div>
              <p className="font-semibold text-gray-900 text-sm">{editUser.full_name}</p>
              <p className="text-gray-500 text-xs">{editUser.email}</p>
            </div>
          </div>
          <form onSubmit={handleEdit} className="space-y-4">
            <Field label="Nome completo">
              <input
                type="text"
                required
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                className={inputCls}
              />
            </Field>
            <Field label="Papel">
              <RoleSelect value={form.role} onChange={(r) => setForm({ ...form, role: r })} />
            </Field>
            <Field label="Status">
              <ActiveToggle value={form.is_active} onChange={(v) => setForm({ ...form, is_active: v })} />
            </Field>
            <ModalFooter onCancel={() => setEditUser(null)} submitting={submitting} label="Salvar Alterações" />
          </form>
        </Modal>
      )}

      {/* ── Change Password Modal ────────────────────────────────────────── */}
      {passwordUser && (
        <Modal title="Alterar Senha" onClose={() => setPasswordUser(null)}>
          <div className="flex items-center gap-3 mb-5 p-3 bg-gray-50 rounded-xl">
            <div className="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center flex-shrink-0">
              <i className="fa-solid fa-key text-amber-600" />
            </div>
            <div>
              <p className="font-semibold text-gray-900 text-sm">{passwordUser.full_name}</p>
              <p className="text-gray-500 text-xs">{passwordUser.email}</p>
            </div>
          </div>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <Field label="Nova senha">
              <input
                type="password"
                required
                minLength={8}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className={inputCls}
                placeholder="Mínimo 8 caracteres"
              />
            </Field>
            <Field label="Confirmar nova senha">
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className={`${inputCls} ${confirmPassword && newPassword !== confirmPassword ? 'border-red-400 focus:ring-red-400' : ''}`}
                placeholder="Repita a senha"
              />
              {confirmPassword && newPassword !== confirmPassword && (
                <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                  <i className="fa-solid fa-triangle-exclamation" /> As senhas não coincidem
                </p>
              )}
            </Field>
            <ModalFooter onCancel={() => setPasswordUser(null)} submitting={submitting} label="Alterar Senha" />
          </form>
        </Modal>
      )}

      {/* ── Delete Confirm Modal ─────────────────────────────────────────── */}
      {deleteUser && (
        <Modal title="Confirmar Exclusão" onClose={() => setDeleteUser(null)}>
          <div className="text-center py-2">
            <div className="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
              <i className="fa-solid fa-trash-can text-red-600 text-xl" />
            </div>
            <p className="text-gray-700 font-medium mb-1">
              Tem certeza que deseja remover <span className="font-bold">{deleteUser.full_name}</span>?
            </p>
            <p className="text-gray-500 text-sm mb-6">
              Esta ação é irreversível e o usuário perderá acesso imediatamente.
            </p>
            <div className="flex gap-3 justify-center">
              <button
                onClick={() => setDeleteUser(null)}
                className="px-5 py-2 rounded-full border border-gray-300 text-gray-700 text-sm font-semibold hover:bg-gray-50 transition"
              >
                Cancelar
              </button>
              <button
                onClick={handleDelete}
                disabled={submitting}
                className="px-5 py-2 rounded-full bg-red-600 text-white text-sm font-semibold hover:bg-red-700 transition disabled:opacity-60"
              >
                {submitting ? <><i className="fa-solid fa-circle-notch fa-spin mr-2" />Removendo…</> : 'Sim, remover'}
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

// ─── Shared UI Atoms ──────────────────────────────────────────────────────────

const inputCls =
  'w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-navy focus:border-transparent transition';

const ActionButton: React.FC<{
  title: string;
  icon: string;
  color: string;
  onClick: () => void;
}> = ({ title, icon, color, onClick }) => (
  <button
    title={title}
    onClick={onClick}
    className={`w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 transition ${color}`}
  >
    <i className={`fa-solid ${icon} text-xs`} />
  </button>
);

const Field: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
  <div>
    <label className="block text-sm font-semibold text-gray-700 mb-1.5">{label}</label>
    {children}
  </div>
);

const RoleSelect: React.FC<{ value: UserRole; onChange: (r: UserRole) => void }> = ({
  value,
  onChange,
}) => (
  <select
    value={value}
    onChange={(e) => onChange(e.target.value as UserRole)}
    className={inputCls}
  >
    <option value="RENTER">Locatário</option>
    <option value="OWNER">Proprietário</option>
    <option value="ADMIN">Administrador</option>
  </select>
);

const ActiveToggle: React.FC<{ value: boolean; onChange: (v: boolean) => void }> = ({
  value,
  onChange,
}) => (
  <button
    type="button"
    onClick={() => onChange(!value)}
    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
      value ? 'bg-emerald-500' : 'bg-gray-300'
    }`}
  >
    <span
      className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
        value ? 'translate-x-6' : 'translate-x-1'
      }`}
    />
    <span className="sr-only">{value ? 'Ativo' : 'Inativo'}</span>
  </button>
);

const Modal: React.FC<{ title: string; onClose: () => void; children: React.ReactNode }> = ({
  title,
  onClose,
  children,
}) => (
  <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4">
    <div className="animate-fadeIn bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
        <h2 className="font-bold text-gray-900">{title}</h2>
        <button
          onClick={onClose}
          className="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-700 transition"
        >
          <i className="fa-solid fa-xmark" />
        </button>
      </div>
      <div className="px-6 py-5">{children}</div>
    </div>
  </div>
);

const ModalFooter: React.FC<{
  onCancel: () => void;
  submitting: boolean;
  label: string;
}> = ({ onCancel, submitting, label }) => (
  <div className="flex gap-3 pt-2">
    <button
      type="button"
      onClick={onCancel}
      className="flex-1 py-2.5 rounded-full border border-gray-300 text-gray-700 text-sm font-semibold hover:bg-gray-50 transition"
    >
      Cancelar
    </button>
    <button
      type="submit"
      disabled={submitting}
      className="flex-1 py-2.5 rounded-full bg-navy text-white text-sm font-semibold hover:bg-gray-800 transition shadow disabled:opacity-60"
    >
      {submitting ? (
        <>
          <i className="fa-solid fa-circle-notch fa-spin mr-2" />
          Salvando…
        </>
      ) : (
        label
      )}
    </button>
  </div>
);

export default UserManagement;
