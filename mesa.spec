# If you're used to Fedora (19ish), here's what's different:
# no nouveau
# no llvmpipe (but m-p-l used for r300/r600/radeonsi)
# bundled glu, manpages, mesa-demos, glx-utils
# three builds of osmesa with pinned soname
# no vdpau drivers
# egl (for glamor), but not gles or wayland

# S390 doesn't have video cards, but we need swrast for xserver's GLX
%ifarch s390 s390x
%define with_hardware 0
%define dri_drivers --with-dri-drivers=swrast
%else
%define with_hardware 1
%define base_drivers swrast,radeon,r200
%ifarch %{ix86}
%define platform_drivers ,i915,i965
%endif
%ifarch x86_64
%define platform_drivers ,i915,i965
%endif
%ifarch ia64
%define platform_drivers ,i915
%endif
%define dri_drivers --with-dri-drivers=%{base_drivers}%{?platform_drivers}
%endif

%define manpages gl-manpages-1.0.1
%define xdriinfo xdriinfo-1.0.2
%define gitdate 20130625
%define demosgitdate 20101028

%define demopkg %{name}-demos-%{demosgitdate}
%define demodir %{_libdir}/mesa

Summary: Mesa graphics libraries
Name: mesa
Version: 9.2
Release: 0.5%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Source0: ftp://ftp.freedesktop.org/pub/mesa/%{version}%{?snapshot}/MesaLib-%{version}%{?snapshot}.tar.bz2
#Source0: http://www.mesa3d.org/beta/MesaLib-%{version}%{?snapshot}.tar.bz2
#Source1: http://www.mesa3d.org/beta/MesaDemos-%{version}%{?snapshot}.tar.bz2
Source0: %{name}-%{gitdate}.tar.xz
Source1: %{name}-demos-%{demosgitdate}.tar.bz2
Source2: %{manpages}.tar.bz2
Source3: make-git-snapshot.sh
Source4: ftp://ftp.freedesktop.org/pub/mesa/glu/glu-9.0.0.tar.bz2
Source5: http://www.x.org/pub/individual/app/%{xdriinfo}.tar.bz2

Patch1: mesa-8.1-osmesa-version.patch
Patch10: mesa-demos-glew-hack.patch
Patch31: mesa-7.6-glx13-app-warning.patch
Patch55: mesa-fix-osmesa.patch
Patch56: mesa-9.2-no-gallium-osmesa.patch

# kwin doesn't work with msaa enabled
Patch57: intel-disable-msaa.patch

# Hush driver load failures when possibly non-local
Patch58: mesa-9.0-hush-driver-load.patch

BuildRequires: pkgconfig autoconf automake libtool
%if %{with_hardware}
BuildRequires: kernel-headers >= 2.6.27-0.305.rc5.git6
BuildRequires: libdrm-devel >= 2.4.37
%endif
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel >= 2.0
BuildRequires: xorg-x11-proto-devel >= 7.1-10
BuildRequires: makedepend
BuildRequires: libselinux-devel
BuildRequires: libXext-devel
BuildRequires: freeglut-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: libxml2-python
BuildRequires: bison flex
BuildRequires: chrpath
BuildRequires: gettext
BuildRequires: libudev-devel
%ifnarch s390 s390x ppc
BuildRequires: mesa-private-llvm-devel
BuildRequires: elfutils-libelf-devel
%endif

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGL
Requires: mesa-dri-drivers%{?_isa} = %{version}-%{release}
%if %{with_hardware}
Requires: libdrm >= 2.4.24-1
Conflicts: xorg-x11-server-Xorg < 1.4.99.901-14
%endif

%description libGL
Mesa libGL runtime library.

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries

%description libEGL
Mesa libEGL runtime libraries

%package dri-filesystem
Summary: Mesa DRI driver filesystem
Group: User Interface/X Hardware Support
%description dri-filesystem
Mesa DRI driver filesystem

%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-dri-filesystem%{?_isa}
Provides: mesa-dri-drivers-experimental = %{version}-%{release}
Obsoletes: mesa-dri-drivers-experimental < %{version}-%{release}
%ifnarch s390 s390x
Requires: mesa-dri1-drivers >= 7.11-6
%endif
%description dri-drivers
Mesa-based DRI drivers.


%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Requires: libX11-devel
Provides: libGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libGL-devel
Mesa libGL development package


%package libEGL-devel
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}
Provides: khrplatform-devel = %{version}-%{release}
Obsoletes: khrplatform-devel < %{version}-%{release}

%description libEGL-devel
Mesa libEGL development package


%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGLU

%description libGLU
Mesa libGLU runtime library


%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
Requires: mesa-libGLU = %{version}-%{release}
Requires: libGL-devel
Provides: libGLU-devel

%description libGLU-devel
Mesa libGLU development package


%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package


%package -n glx-utils
Summary: GLX utilities
Group: Development/Libraries

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.


%package demos
Summary: Mesa demos
Group: Development/Libraries

%description demos
This package provides some demo applications for testing Mesa.


%package libgbm
Summary: Mesa gbm library
Group: System Environment/Libraries
Provides: libgbm

%description libgbm
Mesa gbm runtime library.


%package libgbm-devel
Summary: Mesa libgbm development package
Group: Development/Libraries
Requires: mesa-libgbm%{?_isa} = %{version}-%{release}
Provides: libgbm-devel

%description libgbm-devel
Mesa libgbm development package


%prep
#%setup -q -n Mesa-%{version}%{?snapshot} -b1 -b2 -b5
%setup -q -n mesa-%{gitdate} -b1 -b2 -b4 -b5
grep -q ^/ src/gallium/auxiliary/vl/vl_decoder.c && exit 1
%patch1 -p1 -b .osmesa
%patch31 -p1 -b .glx13-warning
%patch55 -p1 -b .osmesa-fix
%patch56 -p1 -b .gallium-osmesa
%patch57 -p1 -b .nomsaa
%patch58 -p1 -b .hush

sed -i 's/llvm-config/mesa-private-llvm-config-%{__isa_bits}/g' configure.ac
sed -i 's/`$LLVM_CONFIG --version`/&-mesa/' configure.ac

pushd ../%{demopkg}
# make idempotent
rm -f src/glew/Makefile.am
%patch10 -p1 -b .glew-hack
# Hack the demos to use installed data files
sed -i 's,../images,%{_libdir}/mesa,' src/demos/*.c
sed -i 's,geartrain.dat,%{_libdir}/mesa/&,' src/demos/geartrain.c
sed -i 's,isosurf.dat,%{_libdir}/mesa/&,' src/demos/isosurf.c
sed -i 's,terrain.dat,%{_libdir}/mesa/&,' src/demos/terrain.c

popd

%build

# default to dri (not xlib) for libGL on all arches
# XXX please fix upstream
sed -i 's/^default_driver.*$/default_driver="dri"/' configure.ac

autoreconf --install  

export CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"
export CXXFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define common_flags --enable-selinux --enable-pic --disable-asm
%else
%define common_flags --enable-selinux --enable-pic
%endif 
%define osmesa_flags --enable-osmesa %{common_flags} --with-gallium-drivers="" --with-dri-drivers="" --disable-egl --disable-dri

# pick up the 8 bpc from mesa build
%configure %{osmesa_flags} --with-osmesa-bits=16
make SRC_DIRS="mapi/glapi/gen mapi/glapi glsl mesa"
mv %{_lib} osmesa16
make clean

%configure %{osmesa_flags} --with-osmesa-bits=32
make SRC_DIRS="mapi/glapi/gen mapi/glapi glsl mesa"
mv %{_lib} osmesa32
make clean

# just to be sure...
[ `find . -name \*.o | wc -l` -eq 0 ] || exit 1

# XXX should get visibility working again post-dricore.
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

# now build the rest of mesa
%configure %{common_flags} \
    --enable-osmesa \
    --enable-egl \
    --enable-gbm \
    --with-egl-platforms=x11,drm \
    --enable-glx-tls \
    --disable-opencl \
    --disable-xvmc \
    --with-dri-driverdir=%{_libdir}/dri \
    --disable-gallium-egl \
%if %{with_hardware}
%ifnarch ppc
    --enable-gallium-llvm \
    --with-llvm-shared-libs \
    --with-gallium-drivers="r300,r600,radeonsi" \
%else
    --disable-gallium-llvm \
    --with-gallium-drivers="r300,r600" \
%endif
%else
    --with-gallium-drivers="" \
%endif
    %{?dri_drivers}

make #{?_smp_mflags}

pushd ../%{demopkg}
autoreconf -v --install
%configure --bindir=%{demodir}
make %{?_smp_mflags}
popd

pushd ../glu-9.0.0
%configure --disable-static
make %{?_smp_mflags}
popd

pushd ../%{xdriinfo}
%configure
make %{?_smp_mflags}
popd

pushd ../%{manpages}
autoreconf -v --install
%configure
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

# core libs and headers, but not drivers.
make install DESTDIR=$RPM_BUILD_ROOT DRI_DIRS=

# just the DRI drivers that are sane
install -d $RPM_BUILD_ROOT%{_libdir}/dri
[ -f %{_lib}/gallium/r300_dri.so ] && cp %{_lib}/gallium/r300_dri.so %{_lib}/r300_dri.so
[ -f %{_lib}/gallium/r600_dri.so ] && cp %{_lib}/gallium/r600_dri.so %{_lib}/r600_dri.so
for f in i915 i965 r200 r300 r600 radeon swrast; do
    so=%{_lib}/${f}_dri.so
    test -e $so && echo $so
done | xargs install -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/dri >& /dev/null || :

# strip out stupid rpath
chrpath -d $RPM_BUILD_ROOT%{_libdir}/dri/*_dri.so

# strip out undesirable headers
pushd $RPM_BUILD_ROOT%{_includedir}/GL 
rm -f [a-fh-np-wyz]*.h gg*.h glf*.h glew.h glut*.h glxew.h
popd

pushd ../glu-9.0.0
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

# remove .la files
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

pushd ../%{demopkg}
# XXX demos, since they don't install automatically.  should fix that.
install -d $RPM_BUILD_ROOT%{_bindir}
install -m 0755 src/xdemos/glxgears $RPM_BUILD_ROOT%{_bindir}
install -m 0755 src/xdemos/glxinfo $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{demodir}
find src/demos/ -type f -perm /0111 |
    xargs install -m 0755 -t $RPM_BUILD_ROOT/%{demodir}
install -m 0644 src/images/*.rgb $RPM_BUILD_ROOT/%{demodir}
install -m 0644 src/demos/*.dat $RPM_BUILD_ROOT/%{demodir}
popd

# and osmesa
mv osmesa*/* $RPM_BUILD_ROOT%{_libdir}

pushd ../%{xdriinfo}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

# man pages
pushd ../%{manpages}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd $RPM_BUILD_ROOT%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libGLU -p /sbin/ldconfig
%postun libGLU -p /sbin/ldconfig
%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig
%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig
%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig

%files libGL
%defattr(-,root,root,-)
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.*

%files libEGL
%defattr(-,root,root,-)
%{_libdir}/libEGL.so.1
%{_libdir}/libEGL.so.1.*

%files dri-filesystem
%defattr(-,root,root,-)
%doc docs/COPYING
%dir %{_libdir}/dri

%files dri-drivers
%defattr(-,root,root,-)
%if %{with_hardware}
%config(noreplace) %{_sysconfdir}/drirc
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/r300_dri.so
%{_libdir}/dri/r600_dri.so
%ifnarch ppc
%{_libdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64 ia64
%{_libdir}/dri/i915_dri.so
%ifnarch ia64
%{_libdir}/dri/i965_dri.so
%endif
%endif
%endif
%{_libdir}/dri/swrast_dri.so
%{_libdir}/libdricore*.so*
%{_libdir}/libglapi*.so*

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libGL.so
%{_libdir}/pkgconfig/gl.pc
%{_datadir}/man/man3/gl[^uX]*.3gl*
%{_datadir}/man/man3/glX*.3gl*

%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files libGLU
%defattr(-,root,root,-)
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files libGLU-devel
%defattr(-,root,root,-)
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_datadir}/man/man3/glu*.3gl*

%files libOSMesa
%defattr(-,root,root,-)
%{_libdir}/libOSMesa.so.6*
%{_libdir}/libOSMesa16.so.6*
%{_libdir}/libOSMesa32.so.6*

%files libOSMesa-devel
%defattr(-,root,root,-)
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/libOSMesa16.so
%{_libdir}/libOSMesa32.so
%{_libdir}/pkgconfig/osmesa.pc

%files -n glx-utils
%defattr(-,root,root,-)
%{_bindir}/glxgears
%{_bindir}/glxinfo
%{_bindir}/xdriinfo
%{_datadir}/man/man1/xdriinfo.1*

%files demos
%defattr(-,root,root,-)
%{demodir}

%files libgbm
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root,-)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%changelog
* Thu Sep 12 2013 Dave Airlie <airlied@redhat.com> 9.2-0.5
- fix packaging tps test (#1000467)

* Wed Jul 10 2013 Jerome Glisse <ajax@redhat.com> 9.2-0.4
- Fix egl backend flags for glamor

* Wed Jul 10 2013 Jerome Glisse <ajax@redhat.com> 9.2-0.3
- Add libgbm subpackages for glamor

* Wed Jun 26 2013 Adam Jackson <ajax@redhat.com> 9.2-0.2
- Add libEGL subpackages for glamor

* Tue Jun 25 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1
- Rebase to 9.2-pre

* Thu May 30 2013 Dave Airlie <airlied@redhat.com> 9.0-0.9
- CVE-2013-1872: Updated patch from upstream (#963063)

* Wed May 22 2013 Dave Airlie <airlied@redhat.com< 9.0-0.8.1
- CVE-2013-1872: Updated patch (#963063)

* Mon May 20 2013 Dave Airlie <airlied@redhat.com> 9.0-0.8
- CVE-2013-1872: memory corruption oob read/write on intel (#963063)
- CVE-2013-1993: interger overflows in protocol handling (#961613)

* Fri Jan 25 2013 Dave Airlie <airlied@redhat.com> 9.0-0.7
- CVE-2012-5129: heap buffer overflow in glGetUniform* (#903933)

* Thu Jan 24 2013 Adam Jackson <ajax@redhat.com> 9.0-0.6
- Quieten driver load failure messages when the display is possibly non-
  local (#901627)

* Wed Dec 19 2012 Dave Airlie <airlied@redhat.com> 9.0-0.3
- block intel msaa so kwin doesn't regress (#885882)

* Tue Oct 02 2012 Dave Airlie <airlied@redhat.com> 9.0-0.2
- fix mesa-dri-filesystem requires.

* Mon Sep 24 2012 Dave Airlie <airlied@redhat.com> 9.0-0.1
- realign with upstream version for rebase + glu

* Sat Sep 22 2012 Dave Airlie <airlied@redhat.com> 8.1-0.20
- fix osmesa harder, noticed by rpmdiff

* Fri Sep 21 2012 Adam Jackson <ajax@redhat.com> 8.1-0.19
- Fix pthread linkage of glapi and osmesa
- Drop llvmpipe-related patches
- Don't require mesa-dri1-drivers on s390{,x}

* Fri Sep 21 2012 Dave Airlie <airlied@redhat.com> 8.1-0.18
- add mesa-dri1-drivers requires

* Wed Aug 22 2012 Dave Airlie <airlied@redhat.com> 8.1-0.17
- bump for osmesa fixes

* Wed Aug 01 2012 Dave Airlie <airlied@redhat.com> 8.1-0.16
- initial import of 8.1 snapshot from Fedora

* Wed May 16 2012 Dave Airlie <airlied@redhat.com> 7.11-5
- Add missing Ivybridge server PCI ID. (#821873)

* Wed Feb 29 2012 Jerome Glisse <jglisse@redhat.com> 7.11-4
- Resolves: rhbz#788168 (r600g add new pci ids)

* Mon Oct 17 2011 Adam Jackson <ajax@redhat.com> 7.11-3
- Drop nouveau (#745686)

* Thu Oct 06 2011 Adam Jackson <ajax@redhat.com> 7.11-2
- mesa-7.11-b9c7773e.patch: Sync with 7.11 branch
- mesa-7.11-gen6-depth-stalls.patch: Fix GPU hangs on gen6+ in openarena
  and others (#741806)
- Drop tdfx_dri.so, as there's no glide3 package or drm support in el6.

* Tue Aug 09 2011 Adam Jackson <ajax@redhat.com> 7.11-1
- Mesa 7.11 final plus stable backports

* Fri Jul 22 2011 Ben Skeggs <bskeggs@redhat.com> 7.11-0.6
- fix mesa-libGL requires

* Wed Jul 20 2011 Adam Jackson <ajax@redhat.com> 7.11-0.5
- Prov/Obs for -experimental

* Wed Jul 20 2011 Adam Jackson <ajax@redhat.com> 7.11-0.4
- Today's 7.11 branch snapshot, 7.11-rc2 plus one
- Drop (empty) -experimental subpackage

* Mon Jul 18 2011 Adam Jackson <ajax@redhat.com> 7.11-0.3
- Today's 7.11 branch snapshot.

* Wed Jul 13 2011 Adam Jackson <ajax@redhat.com> 7.11-0.2
- Mesa rebase: 7.11-rc1 plus updates through a20a9508 (#713772)

* Fri Jan 14 2011 Dave Airlie <airlied@redhat.com> 7.10-1
- enable Intel Sandybridge support (#667563)

* Mon Apr 12 2010 Dave Airlie <airlied@redhat.com> 7.7-2
- update to mesa 7.7.1 release
