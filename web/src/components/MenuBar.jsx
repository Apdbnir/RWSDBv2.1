import { useState, useRef, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';

/**
 * CUA-compliant Menu Bar Component
 * Implements Common User Access standard for menu navigation
 * - F10 activates menu bar
 * - Alt+underlined letter opens menu
 * - Arrow keys navigate menus
 * - Esc closes menus
 * - Enter selects menu item
 * - Number keys (1-9) select menu items directly when menu is open
 */
const MenuBar = ({
  onFileAction,
  onTableSelect,
  onOperation,
  activeTable,
  activeMenuItem,
  setActiveMenuItem
}) => {
  const { isSuperUser, logout } = useAuth();
  const [openMenu, setOpenMenu] = useState(null);
  const menuBarRef = useRef(null);
  const menuItemRefs = useRef({});

  const menus = [
    {
      id: 'file',
      label: '&File',
      items: [
        { id: 'converter', label: '&DB Converter', shortcut: 'Ctrl+D', icon: 'db' },
        { separator: true },
        { id: 'exit', label: 'E&xit', shortcut: 'Ctrl+E', icon: 'exit' }
      ]
    },
    {
      id: 'databases',
      label: '&Databases',
      items: [
        { id: 'passenger', label: '&1 Passenger', shortcut: 'Alt+D,1', icon: 'passenger' },
        { id: 'train', label: '&2 Train', shortcut: 'Alt+D,2', icon: 'train' },
        { id: 'platform', label: '&3 Platform', shortcut: 'Alt+D,3', icon: 'platform' },
        { id: 'ticket', label: '&4 Ticket', shortcut: 'Alt+D,4', icon: 'ticket' },
        { id: 'schedule', label: '&5 Schedule', shortcut: 'Alt+D,5', icon: 'schedule' },
        { id: 'employee', label: '&6 Employee', shortcut: 'Alt+D,6', icon: 'employee' },
        { id: 'work', label: '&7 Work', shortcut: 'Alt+D,7', icon: 'work' },
        { id: 'service', label: '&8 Service', shortcut: 'Alt+D,8', icon: 'service' },
        { id: 'appointment', label: '&9 Appointment', shortcut: 'Alt+D,9', icon: 'appointment' }
      ]
    },
    {
      id: 'operations',
      label: '&Operations',
      items: [
        { id: 'view', label: '&View', shortcut: 'Ctrl+V', icon: 'view' },
        { separator: true },
        { id: 'add', label: '&Add', shortcut: 'Ctrl+A', icon: 'add', requiresTable: true, superuserOnly: true },
        { id: 'update', label: '&Update', shortcut: 'Ctrl+U', icon: 'update', requiresTable: true, superuserOnly: true },
        { id: 'delete', label: '&Delete', shortcut: 'Ctrl+D', icon: 'delete', requiresTable: true, superuserOnly: true },
        { separator: true },
        { id: 'queries', label: 'S&pecial Queries', shortcut: 'Ctrl+Q', icon: 'queries' },
        { id: 'customQuery', label: '&Custom Query', shortcut: 'Ctrl+Shift+Q', icon: 'custom' },
        { id: 'saveQuery', label: 'Save &Query', shortcut: 'Ctrl+S', icon: 'save', requiresQuery: true, superuserOnly: true },
        { separator: true },
        { id: 'backup', label: '&Backup', shortcut: 'Ctrl+B', icon: 'backup', superuserOnly: true }
      ]
    },
    {
      id: 'export',
      label: 'E&xport',
      items: [
        { id: 'json', label: '&JSON', shortcut: 'Alt+X,J', icon: 'json', superuserOnly: true },
        { id: 'csv', label: '&CSV', shortcut: 'Alt+X,C', icon: 'csv', superuserOnly: true },
        { id: 'excel', label: '&Excel', shortcut: 'Alt+X,E', icon: 'excel', superuserOnly: true }
      ]
    }
  ];

  // Extract mnemonic character from label (text after &)
  const getMnemonic = (label) => {
    const ampersandIndex = label.indexOf('&');
    if (ampersandIndex !== -1 && ampersandIndex < label.length - 1) {
      return label.charAt(ampersandIndex + 1).toUpperCase();
    }
    return null;
  };

  // Render label with underline for mnemonic
  const renderLabel = (label) => {
    const ampersandIndex = label.indexOf('&');
    if (ampersandIndex !== -1 && ampersandIndex < label.length - 1) {
      return (
        <>
          {label.substring(0, ampersandIndex)}
          <span className="underline">{label.charAt(ampersandIndex + 1)}</span>
          {label.substring(ampersandIndex + 2)}
        </>
      );
    }
    return label;
  };

  // Open menu by ID
  const openMenuById = (menuId) => {
    if (openMenu === menuId) {
      setOpenMenu(null);
    } else {
      setOpenMenu(menuId);
      setActiveMenuItem(0);
    }
  };

  // Handle menu item click
  const handleMenuItemClick = (menuId, itemId, item) => {
    if (item.separator) return;

    // Check conditions
    if (item.superuserOnly && !isSuperUser) return;
    if (item.requiresTable && !activeTable) return;

    setOpenMenu(null);

    if (menuId === 'file') {
      if (itemId === 'converter') {
        onOperation('converter');
      } else if (itemId === 'exit') {
        onFileAction('exit');
      }
    } else if (menuId === 'databases') {
      // Only call onTableSelect for actual table items
      const tableItems = ['passenger', 'train', 'platform', 'ticket', 'schedule', 'employee', 'work', 'service', 'appointment'];
      if (tableItems.includes(itemId)) {
        onTableSelect(itemId);
      }
    } else if (menuId === 'operations') {
      onOperation(itemId);
    } else if (menuId === 'export') {
      onOperation(`export_${itemId}`);
    }
  };

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      // F10 - activate menu bar
      if (e.key === 'F10') {
        e.preventDefault();
        if (!openMenu) {
          setOpenMenu('file');
          setActiveMenuItem(0);
        } else {
          setOpenMenu(null);
        }
        return;
      }

      // Alt key combinations for direct menu access
      if (e.altKey && !e.ctrlKey && !e.shiftKey) {
        const key = e.key.toUpperCase();
        const menuIndex = menus.findIndex(m => getMnemonic(m.label) === key);
        if (menuIndex !== -1) {
          e.preventDefault();
          openMenuById(menus[menuIndex].id);
          return;
        }
      }

      // Number keys (1-9) for direct menu item selection when menu is open
      if (openMenu && e.key >= '1' && e.key <= '9') {
        e.preventDefault();
        const currentMenu = menus.find(m => m.id === openMenu);
        if (currentMenu) {
          const menuItems = currentMenu.items.filter(item => !item.separator);
          const selectedIndex = parseInt(e.key) - 1;
          if (selectedIndex >= 0 && selectedIndex < menuItems.length) {
            const selectedItem = menuItems[selectedIndex];
            handleMenuItemClick(openMenu, selectedItem.id, selectedItem);
          }
        }
        return;
      }

      // Escape - close menu
      if (e.key === 'Escape') {
        setOpenMenu(null);
        return;
      }

      // Arrow navigation when menu is open
      if (openMenu) {
        const currentMenu = menus.find(m => m.id === openMenu);
        if (!currentMenu) return;

        const menuItems = currentMenu.items.filter(item => !item.separator);

        if (e.key === 'ArrowDown') {
          e.preventDefault();
          setActiveMenuItem(prev => {
            const next = prev + 1;
            return next >= menuItems.length ? 0 : next;
          });
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          setActiveMenuItem(prev => {
            const next = prev - 1;
            return next < 0 ? menuItems.length - 1 : next;
          });
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          const currentIndex = menus.findIndex(m => m.id === openMenu);
          const nextIndex = currentIndex + 1;
          if (nextIndex < menus.length) {
            setOpenMenu(menus[nextIndex].id);
            setActiveMenuItem(0);
          }
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          const currentIndex = menus.findIndex(m => m.id === openMenu);
          const prevIndex = currentIndex - 1;
          if (prevIndex >= 0) {
            setOpenMenu(menus[prevIndex].id);
            setActiveMenuItem(0);
          }
        } else if (e.key === 'Enter') {
          e.preventDefault();
          const selectedItem = menuItems[activeMenuItem];
          if (selectedItem) {
            handleMenuItemClick(openMenu, selectedItem.id, selectedItem);
          }
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [openMenu, activeMenuItem, menus, activeTable, isSuperUser]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuBarRef.current && !menuBarRef.current.contains(e.target)) {
        setOpenMenu(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <nav 
      ref={menuBarRef}
      className="bg-gray-100 border-b border-gray-300 px-2 py-1 select-none"
      role="menubar"
    >
      <ul className="flex space-x-1 list-none m-0 p-0">
        {menus.map((menu) => (
          <li key={menu.id} className="relative" role="none">
            <button
              ref={el => menuItemRefs.current[menu.id] = el}
              onClick={() => openMenuById(menu.id)}
              className={`px-3 py-1 text-sm rounded transition-colors ${
                openMenu === menu.id 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-700 hover:bg-gray-200'
              }`}
              role="menuitem"
              aria-haspopup="true"
              aria-expanded={openMenu === menu.id}
            >
              {renderLabel(menu.label)}
            </button>

            {/* Dropdown Menu */}
            {openMenu === menu.id && (
              <div
                className="absolute top-full left-0 bg-white border border-gray-300 shadow-lg py-1 min-w-[200px] z-50"
                role="menu"
              >
                {menu.items.map((item, index) => {
                  if (item.separator) {
                    return (
                      <div 
                        key={`sep-${index}`} 
                        className="border-t border-gray-300 my-1"
                        role="separator"
                      />
                    );
                  }

                  // Check if item should be disabled
                  const isDisabled = (
                    (item.superuserOnly && !isSuperUser) ||
                    (item.requiresTable && !activeTable)
                  );

                  const menuItemIndex = menu.items
                    .filter(i => !i.separator)
                    .findIndex(i => i.id === item.id);

                  return (
                    <button
                      key={item.id}
                      onClick={() => handleMenuItemClick(menu.id, item.id, item)}
                      disabled={isDisabled}
                      className={`w-full px-4 py-2 text-left text-sm flex justify-between items-center ${
                        menuItemIndex === activeMenuItem && openMenu === menu.id
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      } ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                      role="menuitem"
                    >
                      <span className="flex items-center gap-3">
                        {renderLabel(item.label)}
                      </span>
                      <span className="text-xs opacity-70">{item.shortcut}</span>
                    </button>
                  );
                })}
              </div>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default MenuBar;
