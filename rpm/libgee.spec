Name:       libgee

Summary:    GObject collection library
Version:    0.6.5
Release:    1
Group:      System/Libraries
License:    LGPLv2+
URL:        http://live.gnome.org/Libgee
Source0:    http://download.gnome.org/sources/%{name}/0.6/%{name}-%{version}.tar.xz
Source100:  libgee.yaml
Patch0:     fix-disable-introspection.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0) >= 2.36.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.36.0
BuildRequires:  vala-devel >= 0.24
BuildRequires:  vala-tools >= 0.24
BuildRequires:  gnome-common

%description
libgee is a collection library providing GObject-based interfaces and
classes for commonly used data structures.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   vala

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}/%{name}

# fix-disable-introspection.patch
%patch0 -p1
# >> setup
echo "EXTRA_DIST = missing-gtk-doc" > gtk-doc.make
# << setup

%build
# >> build pre
touch ChangeLog
USE_GNOME2_MACROS=1 NOCONFIGURE=1 gnome-autogen.sh
# << build pre

%configure --disable-static
make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%doc COPYING
%{_libdir}/*.so.*
# << files

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gee-0.8.pc
%{_datadir}/vala/vapi/gee-0.8.vapi
# << files devel
