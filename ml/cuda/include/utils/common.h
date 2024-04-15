#pragma once
#include <Windows.h>
#include <nlohmann/json.hpp>
#include <string>
#include <vector>

#include "XLogger.h"
#include "tinyxml2.h"
#include "vf/HJWindow.h"
#include "vf_data_def.h"

using json = nlohmann::json;

// 根文件夹
inline const std::string &FBDBaseDir = "FBDTemplateConvert";
inline const std::string &PICBaseDir = "PICConvert";
inline const std::string &PICJSONDir = "json";

inline bool SendCopyDataMsg(CHJCommWindow &wnd, std::string data) {
  COPYDATASTRUCT cd;
  cd.dwData = WM_FBD_TEMPLATE_IMPORT;
  cd.cbData = data.length() + 1;
  cd.lpData = (char *) data.c_str();

  auto lResult = wnd.SendMsg("VFExplorer", WM_COPYDATA, 0, (LPARAM) &cd);
  XLOG_DEBUG("send data: {} with WM_COPYDATA to VFExplorer. result: {}", data, lResult);
  return lResult == Err_TIMEOUT;
}

inline std::string stringToUTF8(const std::string &str) {
  int nwLen = ::MultiByteToWideChar(CP_ACP, 0, str.c_str(), -1, NULL, 0);

  wchar_t *pwBuf = new wchar_t[nwLen + 1];
  ZeroMemory(pwBuf, nwLen * 2 + 2);

  ::MultiByteToWideChar(CP_ACP, 0, str.c_str(), str.length(), pwBuf, nwLen);

  int nLen = ::WideCharToMultiByte(CP_UTF8, 0, pwBuf, -1, NULL, NULL, NULL, NULL);

  char *pBuf = new char[nLen + 1];
  ZeroMemory(pBuf, nLen + 1);

  ::WideCharToMultiByte(CP_UTF8, 0, pwBuf, nwLen, pBuf, nLen, NULL, NULL);

  std::string retStr(pBuf);

  delete[] pwBuf;
  delete[] pBuf;

  pwBuf = NULL;
  pBuf = NULL;

  return retStr;
}

inline std::string UTF8Tostring(const std::string &str) {
  int nwLen = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, NULL, 0);

  wchar_t *pwBuf = new wchar_t[nwLen + 1];
  memset(pwBuf, 0, nwLen * 2 + 2);

  MultiByteToWideChar(CP_UTF8, 0, str.c_str(), str.length(), pwBuf, nwLen);

  int nLen = WideCharToMultiByte(CP_ACP, 0, pwBuf, -1, NULL, NULL, NULL, NULL);

  char *pBuf = new char[nLen + 1];
  memset(pBuf, 0, nLen + 1);

  WideCharToMultiByte(CP_ACP, 0, pwBuf, nwLen, pBuf, nLen, NULL, NULL);

  std::string retStr = pBuf;

  delete[] pBuf;
  delete[] pwBuf;

  pBuf = NULL;
  pwBuf = NULL;

  return retStr;
}

inline std::filesystem::path GetBinPath() {
  char buffer[MAX_PATH];
  // 获取当前执行文件的路径
  GetModuleFileName(NULL, buffer, MAX_PATH);
  // 将路径转换为字符串
  auto binPath = std::filesystem::path(buffer);
  return binPath.parent_path();
}

inline std::filesystem::path getFBDBasePath() {
  auto binPath = GetBinPath();
  binPath.append(FBDBaseDir);
  return binPath;
}

inline bool getVFDefaultProjectDir(std::string &defaultDir) {
  HKEY hKey;
  DWORD rootPathSize = 1024;
  char rootPathData[1024];
  DWORD projectSize = 1024;
  char projectData[1024];
  // 初始化数组
  memset(rootPathData, 0, sizeof(rootPathData));
  memset(projectData, 0, sizeof(projectData));

  defaultDir = "";
  std::filesystem::path vfProjectPath;

  // 打开注册表键
  if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, REG_KEYNAME, 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
    if (RegQueryValueEx(hKey, CFG_ROOT_PATH, NULL, NULL, (LPBYTE) &rootPathData[0], &rootPathSize) == ERROR_SUCCESS) {
      vfProjectPath.append(rootPathData);
    } else {
      XLOG_ERROR("failed to read registry {} value in {}", CFG_ROOT_PATH, REG_KEYNAME);
      return false;
    }

    if (RegQueryValueEx(hKey, CFG_PROJECT, NULL, NULL, (LPBYTE) &projectData[0], &projectSize) == ERROR_SUCCESS) {
      vfProjectPath.append(projectData);
    } else {
      XLOG_ERROR("failed to read registry {} value in {}", CFG_PROJECT, REG_KEYNAME);
      return false;
    }

    RegCloseKey(hKey);
  } else {
    XLOG_ERROR("failed to open registry {} key with error {}", REG_KEYNAME, GetLastError());
    return false;
  }

  XLOG_TRACE("vf default project dir: {}", vfProjectPath.string());
  defaultDir = vfProjectPath.string();
  return true;
}

inline bool getVFDefaultProjectName(const std::string &defaultProjectDir, std::string &defaultProject) {
  if (defaultProjectDir.empty()) {
    return false;
  }

  // 获取 defaultDir 的最后目录
  auto pos = defaultProjectDir.find_last_of('\\');
  if (pos == std::string::npos) {
    XLOG_ERROR("failed to find last \\ in {}", defaultProjectDir);
    return false;
  }

  defaultProject = defaultProjectDir.substr(pos + 1);
  return true;
}

inline bool getVFProjectOAAndCAList(const std::string &projectDir, VFProjectInfo &projectInfo) {
  if (projectDir.empty()) {
    XLOG_ERROR("project dir is empty");
    return false;
  }

  // 从 projectDir 下读取 Project.xml 文件
  std::filesystem::path projectPath(projectDir);
  projectPath.append("Project.xml");
  if (!std::filesystem::exists(projectPath)) {
    XLOG_ERROR("project info file not exists: {}", projectPath.string());
    return false;
  }

  tinyxml2::XMLDocument doc;
  auto ret = doc.LoadFile(projectPath.string().c_str());
  if (ret != tinyxml2::XML_SUCCESS) {
    XLOG_ERROR("failed to load project info file: {}", projectPath.string());
    return false;
  }

  auto projectEle = doc.FirstChildElement("project");
  auto projectName = projectEle->Attribute("name");
  projectInfo.projectName = projectName;
  XLOG_DEBUG("project name: {}", projectName);

  auto controlEle = projectEle->FirstChildElement("control");
  //  遍历以 ctrlarea 命名的节点列表
  for (auto caEle = controlEle->FirstChildElement("ctrlarea"); caEle; caEle = caEle->NextSiblingElement("ctrlarea")) {
    VFControlArea ca;
    ca.name = caEle->Attribute("name");
    ca.description = caEle->Attribute("description");
    XLOG_DEBUG("control area: {}", ca.name);
    XLOG_DEBUG("control area desc: {}", ca.description);

    // 遍历以 ctrlstation 命名的节点列表
    for (auto csEle = caEle->FirstChildElement("ctrlstation"); csEle; csEle = csEle->NextSiblingElement("ctrlstation")) {
      VFControlStation cs;
      cs.name = csEle->Attribute("name");
      cs.description = csEle->Attribute("description");
      XLOG_DEBUG("control station: {}", cs.name);
      XLOG_DEBUG("control station desc: {}", cs.description);
      ca.csList.push_back(cs);
    }

    projectInfo.ctrlAreas.push_back(ca);
  }

  auto hmiEle = projectEle->FirstChildElement("hmi");
  if (!hmiEle) {
    XLOG_ERROR("hmi element not found");
    return false;
  }
  // 遍历以 oparea 命名的节点列表
  for (auto oaEle = hmiEle->FirstChildElement("oparea"); oaEle; oaEle = oaEle->NextSiblingElement("oparea")) {
    VFOperationArea oa;
    oa.name = oaEle->Attribute("name");
    oa.description = oaEle->Attribute("description");
    XLOG_DEBUG("operation area: {}", oa.name);
    XLOG_DEBUG("operation area desc: {}", oa.description);
    projectInfo.opAreas.push_back(oa);
  }

  return true;
}
