/***************************************************************************
                              qgsconfigcache.sip
                              -------------------
  begin                : 2015-05-19
  copyright            : (C) 2015 by Alessandro Pasotti
  email                : a dot pasotti at itopen dot it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

/**
* \class QgsConfigCache
* \brief A cache for xml documents (by configuration file path)
*/


class QgsConfigCache: QObject
{
%TypeHeaderCode
#include "qgsconfigcache.h"
#include "qgsaccesscontrolfilter.h"
%End
  public:
    static QgsConfigCache* instance();
    ~QgsConfigCache();

    QgsServerProjectParser* serverConfiguration( const QString& filePath );
    QgsWfsProjectParser* wfsConfiguration( const QString& filePath, const QgsAccessControl* accessControl );
    QgsWmsConfigParser* wmsConfiguration( const QString& filePath, const QgsAccessControl* accessControl, const QMap<QString, QString>& parameterMap = QMap< QString, QString >() );

  private:
    QgsConfigCache();

};


